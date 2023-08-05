import numpy as np
import cv2
import os.path as osp


class FaceDetection(object):
    def __init__(self, threshold=0.4, nms_thresh=0.3, max_size=960):
        onnx_path = osp.join(osp.dirname(__file__), "centerface.onnx")
        self.net = cv2.dnn.readNetFromONNX(onnx_path)
        self.img_h_new, self.img_w_new, self.scale_h, self.scale_w = 0, 0, 0, 0
        self.threshold = threshold
        self.nms_thresh = nms_thresh
        self.max_size = max_size

    def __call__(self, bgr_img, showresult=False):
        height, width = bgr_img.shape[:2]
        self.img_h_new, self.img_w_new, self.scale_h, self.scale_w = self.transform(height, width)
        dets, lms = self.inference_opencv(bgr_img)
        boxes = dets[:, :4].astype(np.int)
        scores = dets[:, -1]
        lms = lms.astype(np.int)
        if not showresult:
            return boxes, scores, lms

        for box in boxes:
            cv2.rectangle(bgr_img, (box[0], box[1]), (box[2], box[3]), (2, 255, 0), 1)
        for lm in lms:
            for i in range(0, 5):
                cv2.circle(bgr_img, (lm[i * 2], lm[i * 2 + 1]), 2, (0, 0, 255), -1)
        cv2.imshow('detection result', bgr_img)
        cv2.waitKey(0)

        return boxes, scores, lms

    def demo(self):
        test_image_path = osp.join(osp.dirname(__file__), "test.jpg")
        bgr_image = cv2.imread(test_image_path)
        self.__call__(bgr_image, showresult=True)

    def inference_opencv(self, img):
        blob = cv2.dnn.blobFromImage(img, scalefactor=1.0,
                                     size=(self.img_w_new, self.img_h_new),
                                     mean=(0, 0, 0), swapRB=True, crop=False)
        self.net.setInput(blob)
        heatmap, scale, offset, lms = self.net.forward(["537", "538", "539", '540'])
        return self.postprocess(heatmap, lms, offset, scale)

    def transform(self, h, w):
        if h > w:
            img_h_new = self.max_size
            img_w_new = int(np.ceil(w * img_h_new / h / 32) * 32)
        else:
            img_w_new = self.max_size
            img_h_new = int(np.ceil(h * img_w_new / w / 32) * 32)

        scale_h, scale_w = img_h_new / h, img_w_new / w
        return img_h_new, img_w_new, scale_h, scale_w

    def postprocess(self, heatmap, lms, offset, scale):
        dets, lms = self.decode(heatmap, scale, offset, lms, (self.img_h_new, self.img_w_new),
                                threshold=self.threshold, nms_thresh=self.nms_thresh)
        if len(dets) > 0:
            dets[:, 0:4:2], dets[:, 1:4:2] = dets[:, 0:4:2] / self.scale_w, dets[:, 1:4:2] / self.scale_h
            lms[:, 0:10:2], lms[:, 1:10:2] = lms[:, 0:10:2] / self.scale_w, lms[:, 1:10:2] / self.scale_h
        else:
            dets = np.empty(shape=[0, 5], dtype=np.float32)
            lms = np.empty(shape=[0, 10], dtype=np.float32)

        return dets, lms

    def decode(self, heatmap, scale, offset, landmark, size, threshold=0.1, nms_thresh=0.3):
        heatmap = np.squeeze(heatmap)
        scale0, scale1 = scale[0, 0, :, :], scale[0, 1, :, :]
        offset0, offset1 = offset[0, 0, :, :], offset[0, 1, :, :]
        c0, c1 = np.where(heatmap > threshold)
        boxes, lms = [], []

        if len(c0) > 0:
            for i in range(len(c0)):
                s0, s1 = np.exp(scale0[c0[i], c1[i]]) * 4, np.exp(scale1[c0[i], c1[i]]) * 4
                o0, o1 = offset0[c0[i], c1[i]], offset1[c0[i], c1[i]]
                s = heatmap[c0[i], c1[i]]
                x1, y1 = max(0, (c1[i] + o1 + 0.5) * 4 - s1 / 2), max(0, (c0[i] + o0 + 0.5) * 4 - s0 / 2)
                x1, y1 = min(x1, size[1]), min(y1, size[0])
                boxes.append([x1, y1, min(x1 + s1, size[1]), min(y1 + s0, size[0]), s])
                lm = []
                for j in range(5):
                    lm.append(landmark[0, j * 2 + 1, c0[i], c1[i]] * s1 + x1)
                    lm.append(landmark[0, j * 2, c0[i], c1[i]] * s0 + y1)
                lms.append(lm)
            boxes = np.asarray(boxes, dtype=np.float32)
            keep = self.nms(boxes[:, :4], boxes[:, 4], nms_thresh)

            boxes = boxes[keep, :]
            lms = np.asarray(lms, dtype=np.float32)
            lms = lms[keep, :]
        return boxes, lms

    def nms(self, boxes, scores, nms_thresh):
        x1 = boxes[:, 0]
        y1 = boxes[:, 1]
        x2 = boxes[:, 2]
        y2 = boxes[:, 3]
        areas = (x2 - x1 + 1) * (y2 - y1 + 1)
        order = np.argsort(scores)[::-1]
        num_detections = boxes.shape[0]
        suppressed = np.zeros((num_detections,), dtype=np.bool)

        keep = []
        for _i in range(num_detections):
            i = order[_i]
            if suppressed[i]:
                continue
            keep.append(i)

            ix1 = x1[i]
            iy1 = y1[i]
            ix2 = x2[i]
            iy2 = y2[i]
            iarea = areas[i]

            for _j in range(_i + 1, num_detections):
                j = order[_j]
                if suppressed[j]:
                    continue

                xx1 = max(ix1, x1[j])
                yy1 = max(iy1, y1[j])
                xx2 = min(ix2, x2[j])
                yy2 = min(iy2, y2[j])
                w = max(0, xx2 - xx1 + 1)
                h = max(0, yy2 - yy1 + 1)

                inter = w * h
                ovr = inter / (iarea + areas[j] - inter)
                if ovr >= nms_thresh:
                    suppressed[j] = True

        return keep


if __name__ == "__main__":
    import time
    frame = cv2.imread('test.jpg')
    centerface = FaceDetection()
    st = time.time()
    centerface(frame, showresult=True)
    print(time.time() - st)
