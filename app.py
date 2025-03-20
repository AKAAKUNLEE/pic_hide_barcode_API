from flask import Flask, request, send_file
from PIL import Image
import io

app = Flask(__name__)

@app.route('/api/merge', methods=['POST'])
def merge_images():
    try:
        # 从请求中获取上传的文件
        img_putong = request.files['img_putong']
        img_barcode = request.files['img_barcode']

        # 打开图片
        imgPutong = Image.open(img_putong)
        imgBarcode = Image.open(img_barcode)

        # 创建新图片
        imgMix = Image.new("RGBA", (imgPutong.width, imgPutong.height))

        # 填充新图片的像素
        for w in range(imgMix.width):
            for h in range(imgMix.height):
                pxlPutong = imgPutong.getpixel((w, h))
                pxlBarcode = imgBarcode.getpixel((w, h))

                if pxlBarcode[0] > 200:
                    imgMix.putpixel((w, h), (pxlPutong[0], pxlPutong[1], pxlPutong[2], 255))
                else:
                    alpha = 150
                    imgMix.putpixel((w, h), (
                        int((pxlPutong[0] - (255 - alpha)) / alpha * 255),
                        int((pxlPutong[1] - (255 - alpha)) / alpha * 255),
                        int((pxlPutong[2] - (255 - alpha)) / alpha * 255),
                        alpha))

        # 将合成图片保存到内存中
        img_byte_arr = io.BytesIO()
        imgMix.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)

        # 返回图片文件
        return send_file(img_byte_arr, mimetype='image/png')

    except Exception as e:
        return {"error": str(e)}, 500

if __name__ == '__main__':
    app.run(debug=True)
