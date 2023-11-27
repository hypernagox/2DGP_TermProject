from src.Singletons.core import CCore


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
        self.cw,self.ch = CCore().width,CCore().height
        self.w,self.h =  self.layer_img.w,self.layer_img.h
    def GetTransform(self):
        return self.transform

    def update(self):
        pass

    def calculate_infinite_scrolling(self, camera_x, screen_width, screen_height, image_width, image_height):
        start_x = -(camera_x % image_width)
        num_images = int(screen_width / image_width) + 2

        images_info = []
        for i in range(num_images):
            screen_start_x = start_x + i * image_width
            draw_width = min(image_width, screen_width - screen_start_x)
            draw_height = screen_height
            image_start_x = max(0, -screen_start_x)
            image_info = ((screen_start_x, 0), (draw_width, draw_height), (image_start_x, 0))
            images_info.append(image_info)
        return images_info

    def render(self):
        from src.Components.camera import CCamera
        cam_x = CCamera.curMainCam.m_transform.m_pos.x
        desired_width = 300
        desired_height = 300
        for img_info in self.calculate_infinite_scrolling(cam_x, self.cw, self.ch, self.w, self.h):
            screen_start, draw_size, image_start = img_info

            clip_left = max(0, int(image_start[0]))
            clip_bottom = max(0, int(image_start[1]))
            clip_width = min(int(draw_size[0]), self.w - clip_left)
            clip_height = int(draw_size[1])

            screen_x = max(0, int(screen_start[0]))
            screen_y = int(screen_start[1])

            self.layer_img.clip_draw_to_origin(
                left=clip_left,
                bottom=clip_bottom,
                width=clip_width,
                height=clip_height,
                x=screen_x,
                y=screen_y,
            )