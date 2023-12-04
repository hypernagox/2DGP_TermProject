from Singletons.core import CCore
#from src.struct.vector2 import Vec2


class CLayer:
    def __init__(self,fileName,filelb,filert,worldLeftBottom,width,height):
        from Singletons.resourcemgr import CResMgr
        self.layer_img = CResMgr().GetTex(fileName)
        self.left = filelb.x
        self.bottom = filelb.y
        self.right = filert.x
        self.top = filert.y
        from Components.spriterenderer import CSpriteRenderer
        self.sprite_renderer = CSpriteRenderer()
        from Components.transform import CTransform
        self.transform = CTransform()
        self.transform.m_size.x = width
        self.transform.m_size.y = height
        self.transform.m_pos.x = worldLeftBottom.x + width / 2
        self.transform.m_pos.y = worldLeftBottom.y + height / 2
        self.sprite_renderer.owner = self.transform.owner = self

        self.x_min = worldLeftBottom.x
        self.x_max = worldLeftBottom.x + width
        self.speed = 1
        self.cw,self.ch = CCore().width  ,CCore().height
        self.w,self.h =  self.layer_img.w,self.layer_img.h

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
        from Components.camera import CCamera
        cam_x = int(CCamera.curMainCam.GetCamPos().x)
        screen_width = int(self.cw)
        image_width = int(self.layer_img.w)
        image_height = int(self.layer_img.h)


        scale_factor = screen_width / image_width
        new_image_width = int(image_width * scale_factor)
        new_image_height = int(image_height * scale_factor)


        scroll_x = -(cam_x % new_image_width)


        start_x = scroll_x if scroll_x <= 0 else scroll_x - new_image_width

        while start_x < screen_width:
            #clip_width = min(new_image_width, screen_width - start_x)
            self.layer_img.clip_draw_to_origin(
                left=0,
                bottom=0,
                width=self.cw,
                height=new_image_height,
                x=start_x,
                y=0,
                w=self.cw,
                h=700
            )
            start_x += new_image_width