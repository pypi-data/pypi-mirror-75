from typing import Optional
import time

from PIL import Image, ImageDraw, ImageFont

from .utils import pil_utils as piu
from .utils import reddit_image_utils as riu

from .compact_image import CompactImage
from .models.relative_position import RelativePosition
from .models.vote import Vote
# from .pil_utils import text_wrap, image, text_image

class RedditImage:
    # RESOURCES PATHS
    __RESOURCES_PATH        = 'resources'
    __FONTS_RESOURCES_PATH  = __RESOURCES_PATH + '/' + 'fonts'
    __IMAGES_RESOURCES_PATH = __RESOURCES_PATH + '/' + 'images'

    def __init__(
        self,

        # FONTS
        FONT_PATH_REGULAR: Optional[str]            = None,
        FONT_PATH_BOLD: Optional[str]               = None,
        FONT_PATH_BOLDEST: Optional[str]            = None,
        FONT_PATH_THUMBNAIL: Optional[str]          = None,

        # IMAGES
        IMAGE_PATH_UPVOTE: Optional[str]            = None,
        IMAGE_PATH_UPVOTE_COLORED: Optional[str]    = None,
        IMAGE_PATH_DOWNVOTE: Optional[str]          = None,
        IMAGE_PATH_DOWNVOTE_COLORED: Optional[str]  = None,

        # FONT SIZES
        FONT_SIZE_HEADER: int                       = 24,
        FONT_SIZE_TITLE: int                        = 50,
        FONT_SIZE_SUBTITLE: int                     = 28,
        FONT_SIZE_COMMENT: int                      = 28,
        FONT_SIZE_VOTES: int                        = 30,

        FONT_SIZE_THUMBNAIL_SUB: int                = 100,
        FONT_SIZE_THUMBNAIL_TITLE: int              = 150,

        # COLORS
        COLOR_BG: (int, int, int, int)              = (20, 20, 21, 255),
        COLOR_TEXT_LIGHT: (int, int, int)           = (205, 209, 212),
        COLOR_TEXT_DARK: (int, int, int)            = (109, 112, 113),

        # DISTANCES
        DISTANCE: int                               = 10,
        PADDING: Optional[int]                      = None,
        PADDING_THUMBNAIL: Optional[int]            = None,
        COMMENT_OFFSET: Optional[int]               = None,
    ):
        self.FONT_PATH_REGULAR = FONT_PATH_REGULAR or self.__path(self.__FONTS_RESOURCES_PATH + '/regular.ttf')
        self.FONT_PATH_BOLD = FONT_PATH_BOLD or self.__path(self.__FONTS_RESOURCES_PATH + '/bold.ttf')
        self.FONT_PATH_BOLDEST = FONT_PATH_BOLDEST or self.__path(self.__FONTS_RESOURCES_PATH + '/boldest.ttf')
        self.FONT_PATH_THUMBNAIL = FONT_PATH_THUMBNAIL or self.__path(self.__FONTS_RESOURCES_PATH + '/thumbnail.ttf')

        self.IMAGE_PATH_UPVOTE = IMAGE_PATH_UPVOTE or self.__path(self.__IMAGES_RESOURCES_PATH + '/up.png')
        self.IMAGE_PATH_UPVOTE_COLORED = IMAGE_PATH_UPVOTE_COLORED or self.__path(self.__IMAGES_RESOURCES_PATH + '/up-colored.png')
        self.IMAGE_PATH_DOWNVOTE = IMAGE_PATH_DOWNVOTE or self.__path(self.__IMAGES_RESOURCES_PATH + '/down.png')
        self.IMAGE_PATH_DOWNVOTE_COLORED = IMAGE_PATH_DOWNVOTE_COLORED or self.__path(self.__IMAGES_RESOURCES_PATH + '/down-colored.png')

        self.FONT_SIZE_HEADER = FONT_SIZE_HEADER
        self.FONT_SIZE_TITLE = FONT_SIZE_TITLE
        self.FONT_SIZE_SUBTITLE = FONT_SIZE_SUBTITLE
        self.FONT_SIZE_COMMENT = FONT_SIZE_COMMENT
        self.FONT_SIZE_VOTES = FONT_SIZE_VOTES

        self.FONT_SIZE_THUMBNAIL_SUB = FONT_SIZE_THUMBNAIL_SUB
        self.FONT_SIZE_THUMBNAIL_TITLE = FONT_SIZE_THUMBNAIL_TITLE

        self.COLOR_BG = COLOR_BG
        self.COLOR_TEXT_LIGHT = COLOR_TEXT_LIGHT
        self.COLOR_TEXT_DARK = COLOR_TEXT_DARK

        self.DISTANCE = DISTANCE
        self.PADDING = PADDING or 2*DISTANCE
        self.PADDING_THUMBNAIL = PADDING_THUMBNAIL or 5*DISTANCE
        self.COMMENT_OFFSET = COMMENT_OFFSET or 10*DISTANCE

    def bg_image(self, width: int, height: int) -> Image:
        return piu.image(width, height, self.COLOR_BG)

    def create_title(
        self,
        title: str,
        upvotes: int,
        sub: str,
        poster_username: str,
        timestamp: float,
        width: int,
        height: Optional[int] = None,
        user_vote: Vote = Vote.NONE
    ) -> Image:
        sub_font    = ImageFont.truetype(self.FONT_PATH_BOLDEST, self.FONT_SIZE_HEADER)
        header_font = ImageFont.truetype(self.FONT_PATH_BOLD,    self.FONT_SIZE_HEADER)
        title_font  = ImageFont.truetype(self.FONT_PATH_BOLD,    self.FONT_SIZE_TITLE)

        votes_img = self.__votes_image(64, upvotes=upvotes, user_vote=user_vote)
        ci = CompactImage(self.DISTANCE, self.PADDING, bg_color=self.COLOR_BG, image=votes_img)

        sub_img = piu.text_image(riu.sub(sub), sub_font, fg_color=self.COLOR_TEXT_LIGHT, wrap_instead_of_font_downscale=False)
        ci.add_image(sub_img, positioned=RelativePosition.Right, to_image=votes_img, extra_distance_x=int(1.5*self.DISTANCE))

        header_str = '· Posted by ' + riu.username(poster_username) + ' · ' + riu.date_text(timestamp) + ' ago'
        header_img = piu.text_image(header_str, header_font, height=sub_img.size[1], fg_color=self.COLOR_TEXT_DARK,wrap_instead_of_font_downscale=False)
        ci.add_image(header_img, positioned=RelativePosition.Right, to_image=sub_img, centered=True)

        title_img = piu.text_image(title, title_font, width=width-votes_img.size[0] - 2*self.PADDING - self.DISTANCE, fg_color=self.COLOR_TEXT_LIGHT, wrap_instead_of_font_downscale=True)
        ci.add_image(title_img, positioned=RelativePosition.Bottom, to_image=sub_img)
        ci.add_image(self.__footer_img, positioned=RelativePosition.Bottom, to_image=title_img)

        return ci.render(width=width, container_height=height)

    def create_subtitle(
        self,
        subtitle: str,
        width: int,
        height: Optional[int] = None
    ) -> Image:
        return CompactImage(
            self.DISTANCE,
            2*self.PADDING,
            bg_color=self.COLOR_BG, 
            image=piu.text_image(
                subtitle,
                ImageFont.truetype(self.FONT_PATH_BOLD, self.FONT_SIZE_SUBTITLE),
                fg_color=self.COLOR_TEXT_LIGHT,
                wrap_instead_of_font_downscale=True,
                width=width - 4*self.PADDING
            )
        ).render(width=width, container_height=height)

    def create_thumbnail(
        self,
        title: str,
        sub: str,
        image_overlay_path: str,
        width: int = 1920,
        height: int = 1080
    ) -> Image:
        from colorthief import ColorThief
        overlay_len_perc = 0.4
        text_len_perc = 1.0 - overlay_len_perc
        overlay = piu.resized(Image.open(image_overlay_path).convert("RGBA"), width=int(float(width)*overlay_len_perc), height=height - self.PADDING_THUMBNAIL)
        # dominant_color = ColorThief(image_overlay_path).get_color(quality=1)
        # print(dominant_color)
        dominant_color = riu.saturate_color(ColorThief(image_overlay_path).get_color(quality=1))

        bg_img = piu.image(width, height, self.COLOR_BG)
        bg_img.paste(overlay, (width-overlay.size[0], height-overlay.size[1]), overlay)

        sub_img = piu.text_image(riu.sub(sub), ImageFont.truetype(self.FONT_PATH_THUMBNAIL, self.FONT_SIZE_THUMBNAIL_SUB), fg_color=self.COLOR_TEXT_LIGHT, wrap_instead_of_font_downscale=False)
        ci = CompactImage(
            self.DISTANCE,
            self.PADDING_THUMBNAIL,
            sub_img
        )

        # halo_col = (0, 0, 0)   # black
        # halo_col = (255, 255, 255)

        title_img = piu.text_image(
            title,
            ImageFont.truetype(self.FONT_PATH_THUMBNAIL, self.FONT_SIZE_THUMBNAIL_TITLE),
            fg_color=dominant_color,
            wrap_instead_of_font_downscale=True,
            width=int(float(width)*text_len_perc) - self.PADDING_THUMBNAIL - self.DISTANCE,
            height=height - sub_img.size[1] - self.PADDING_THUMBNAIL - self.DISTANCE,
            # halo_color=halo_col#(255, 255, 255, 255)
        )
        title_img_extra_distance_y = int((float(height - self.PADDING_THUMBNAIL - self.DISTANCE - sub_img.size[1]) - title_img.size[1])/2)

        ci.add_image(title_img, positioned=RelativePosition.Bottom, to_image=sub_img, extra_distance_y=title_img_extra_distance_y)
        rendered = ci.render(width=int(float(width)*text_len_perc) - self.DISTANCE, height=height)

        bg_img.paste(rendered, (0,0), rendered)

        return bg_img

    def create_comment(
        self,
        content: str,
        upvotes: int,
        poster_username: str,
        timestamp: float,
        width: int,
        height: Optional[int] = None,
        comment_level: int = 0,
        user_vote: Vote = Vote.NONE
    ) -> Image:
        username_font   = ImageFont.truetype(self.FONT_PATH_BOLDEST, self.FONT_SIZE_HEADER)
        header_font     = ImageFont.truetype(self.FONT_PATH_BOLD,    self.FONT_SIZE_HEADER)
        comment_font    = ImageFont.truetype(self.FONT_PATH_BOLD, self.FONT_SIZE_COMMENT)

        votes_img = self.__votes_image(40, user_vote=user_vote)
        ci = CompactImage(self.DISTANCE, self.PADDING, bg_color=self.COLOR_BG)
        ci.add_image(votes_img, extra_distance_x=comment_level*self.COMMENT_OFFSET)

        username_img = piu.text_image(riu.username(poster_username), username_font, fg_color=self.COLOR_TEXT_LIGHT, wrap_instead_of_font_downscale=False)
        ci.add_image(username_img, positioned=RelativePosition.Right, to_image=votes_img, extra_distance_x=int(1.5*self.DISTANCE))

        header_img = piu.text_image(riu.number_text(upvotes) + ' points · ' + riu.date_text(timestamp) + ' ago', header_font, height=username_img.size[1], fg_color=self.COLOR_TEXT_DARK,wrap_instead_of_font_downscale=False)
        ci.add_image(header_img, positioned=RelativePosition.Right, to_image=username_img, centered=True)

        content_img = piu.text_image(content, comment_font, width=width-votes_img.size[0] - 2*self.PADDING - self.DISTANCE, fg_color=self.COLOR_TEXT_LIGHT, wrap_instead_of_font_downscale=True)
        ci.add_image(content_img, positioned=RelativePosition.Bottom, to_image=username_img)
        ci.add_image(self.__footer_img, positioned=RelativePosition.Bottom, to_image=content_img)

        return ci.render(width=width, container_height=height)


    @property
    def __footer_img(self) -> Image:
        try:
            return self.___footer_img
        except AttributeError:
            self.___footer_img = piu.text_image(
                'Reply   Give Award   Share   Report   Save',
                ImageFont.truetype(self.FONT_PATH_BOLD, self.FONT_SIZE_HEADER),
                fg_color=self.COLOR_TEXT_DARK,
                wrap_instead_of_font_downscale=False
            )

            return self.___footer_img

    def __votes_image(self, width: int, upvotes: Optional[int] = None, user_vote: Vote = Vote.NONE) -> Image:
        img_upvote = Image.open(self.IMAGE_PATH_UPVOTE)
        img_upvote.thumbnail((width, width), Image.ANTIALIAS)
        img_downvote = Image.open(self.IMAGE_PATH_DOWNVOTE)
        img_downvote.thumbnail((width, width), Image.ANTIALIAS)

        ci = CompactImage(self.DISTANCE, 0, image=img_upvote)

        img_votes = None

        if upvotes is not None:
            img_votes = piu.text_image(
                riu.number_text(upvotes),
                ImageFont.truetype(self.FONT_PATH_BOLDEST, self.FONT_SIZE_VOTES),
                width=int(float(width)*1.5),
                fg_color=self.COLOR_TEXT_LIGHT,
                wrap_instead_of_font_downscale=False,
                align='center'
            )

            ci.add_image(img_votes, positioned=RelativePosition.Bottom, to_image=img_upvote, centered=True)

        ci.add_image(img_downvote, positioned=RelativePosition.Bottom, to_image=img_votes if img_votes is not None else img_upvote, centered=True)

        return ci.render()


    @staticmethod
    def __path(sub_path: str) -> str:
        import os

        return os.path.join(os.path.dirname(os.path.abspath(__file__)), sub_path)