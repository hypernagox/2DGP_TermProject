from src.Singletons.core import CCore
from src.struct.vector2 import Vec2


class CLayer:
    def __init__(self,fileName,filelb,filert,worldLeftBottom,width,height):
        from src.Singletons.resourcemgr import CResMgr
        self.layer_img = CResMgr().GetTex(fileName)
        self.left = filelb.x
        self.bottom = filelb.y
        self.right = filert.x
        self.top = filert.y
        from src.Components.spriterenderer import CSpriteRenderer
        self.sprite_renderer = CSpriteRenderer()
        from src.Components.transform import CTransform
        self.transform = CTransform()
        self.transform.m_size.x = width
        self.transform.m_size.y = height
        self.transform.m_pos.x = worldLeftBottom.x + width / 2
        self.transform.m_pos.y = worldLeftBottom.y + height / 2
        self.sprite_renderer.owner = self.transform.owner = self

        self.x_min = worldLeftBottom.x
        self.x_max = worldLeftBottom.x + width
        self.speed = 1
        self.cw,self.ch = CCore().width * 2 ,CCore().height * 2
        self.w,self.h =  self.layer_img.w ,self.layer_img.h

        # 비율
        # 필요한 재료?
        #
        # 사진 너비
        # 카메라 x
        #
    def GetTransform(self):
        return self.transform

    def update(self):
        pass

    def calculate_infinite_scrolling(self, camera_x, camera_y, screen_width, screen_height, image_width, image_height):
        start_x = -(int(camera_x * self.speed) % image_width)
        start_y = -camera_y

        num_images = int(screen_width / image_width) + 2

        images_info = []
        for i in range(num_images):
            screen_start_x = start_x + i * image_width
            draw_width = min(image_width, screen_width - screen_start_x) # 비율만큼
            draw_height = screen_height
            image_start_x = max(0, -screen_start_x)
            image_info = ((screen_start_x, start_y), (draw_width, draw_height), (image_start_x, start_y))
            images_info.append(image_info)

        return images_info

    def render(self):
        from src.Components.camera import CCamera
        mainCam = CCamera().curMainCam
        cam_x = CCamera.curMainCam.GetCamPos().x
        cam_y = CCamera.curMainCam.GetCamPos().y
        # 비율맞춰서
        # 원본이미지 너비 * 실제월드에서의크기 / (상수)
        # 높이 똑같음

        # bl  = 내 스크린 기준 LB를 월드로 바꾼좌표 (스크린투월드)
        # tr = RT 는 내 화면 크기넓이 이것도 스크린투월드

        # begin x 사진의 시작 left 스크린좌표기준
        # wv 오프셋 - bl - w(원본이미지너비) * 0.5) % w - w + bl.x
        # n 몇번 그리는지 계산 << n = (오른쪽가장자리 - 왼쪽처음)/w << 이걸 ceil

        # v = vec2(bx * (tx(레인지) * w(이미지너비),y오프셋)
        bl = mainCam.screen_to_world(Vec2())
        tr = mainCam.screen_to_world(Vec2(1400,700))
        bx = (1400 - bl.x - self.w * 0.5) % self.w - self.w + bl.x
        self.layer_img.clip_draw_to_origin(
            0,
            0,

        )
        # for img_info in self.calculate_infinite_scrolling(cam_x, cam_y, self.cw , self.ch, self.w, self.h):
        #     screen_start, draw_size, image_start = img_info
        #
        #
        #     # 비율맞춰서
        #     # 원본이미지 너비 * 실제월드에서의크기 / (상수)
        #     # 높이 똑같음
        #
        #     # bl  = 내 스크린 기준 LB를 월드로 바꾼좌표 (스크린투월드)
        #     # tr = RT 는 내 화면 크기넓이 이것도 스크린투월드
        #
        #     # begin x 사진의 시작 left 스크린좌표기준
        #     # wv 오프셋 - bl - w(원본이미지너비) * 0.5) % w - w + bl.x
        #     # n 몇번 그리는지 계산 << n = (오른쪽가장자리 - 왼쪽처음)/w << 이걸 ceil
        #
        #     # v = vec2(bx * (tx(레인지) * w(이미지너비),y오프셋)
        #
        #
        #     clip_left = max(0, int(image_start[0]))
        #     clip_bottom = max(0, int(image_start[1]))
        #     clip_width = min(int(draw_size[0]), self.w - clip_left)
        #     clip_height = int(self.h) * 2
        #
        #     screen_x = max(0, int(screen_start[0]))
        #     screen_y = int(screen_start[1])
        #
        #     self.layer_img.clip_draw_to_origin(
        #         left=clip_left,
        #         bottom=clip_bottom,
        #         width=clip_width,
        #         height=clip_height,
        #         x=screen_x,
        #         y=screen_y,
        #     )