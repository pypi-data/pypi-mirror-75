"""
main application class for GUIApp-conform Kivy app
==================================================

This ae portion is providing two classes (:class:`FrameworkApp`
and :class:`KivyMainApp`) and some useful constants.

The class :class:`KivyMainApp` is implementing a main app
class that is reducing the amount of code needed for
to create a Python application based on the
:ref:`kivy framework<kivy.org>`.

:class:`KivyMainApp` is based on the following classes:

* the abstract base class :class:`~ae.gui_app.MainAppBase`
  which adds the concepts of :ref:`application status`
  (including :ref:`app-state-variables` and :ref:`app-state-constants`),
  :ref:`application flow` and :ref:`application events`.
* the class :class:`~ae.console.ConsoleApp` is adding
  :ref:`config-files`, :ref:`config-variables`
  and :ref:`config-options`.
* the class :class:`~ae.core.AppBase` is adding
  :ref:`application logging` and :ref:`application debugging`.


The main app class :class:`KivyMainApp` is also encapsulating the
:class:`Kivy app class <kivy.app.App>` within the :class:`FrameworkApp`.
An instance of the Kivy app class can be directly accessed from
the main app class instance via the
:attr:`~KivyMainApp.framework_app` attribute.


unit tests
----------

For to run the unit tests of this ae portion you need a system
with a graphic system supporting at least V 2.0 of OpenGL and the
kivy framework installed.

.. note::
    unit tests does have 100 % coverage but are currently not passing the gitlab CI
    tests because we failing in setup a proper running window system on the
    python image that all ae portions are using.

Any help for to fix the problems with the used gitlab CI image is highly appreciated.

"""
import os
from typing import Callable, List, Optional, Tuple, Type, Union

from plyer import storagepath, vibrator                                     # type: ignore

import kivy                                                                 # type: ignore
from kivy.app import App                                                    # type: ignore
from kivy.clock import Clock                                                # type: ignore
from kivy.core.audio import SoundLoader                                     # type: ignore
from kivy.core.window import Window                                         # type: ignore
from kivy.factory import Factory, FactoryException                          # type: ignore
from kivy.input import MotionEvent                                          # type: ignore
from kivy.lang import Builder, Observable                                   # type: ignore
# pylint: disable=no-name-in-module
from kivy.properties import BooleanProperty, DictProperty, ListProperty, ObjectProperty, StringProperty  # type: ignore
from kivy.uix.behaviors import ButtonBehavior                               # type: ignore
from kivy.uix.dropdown import DropDown                                      # type: ignore
from kivy.uix.label import Label                                            # type: ignore
from kivy.uix.popup import Popup                                            # type: ignore
from kivy.uix.widget import Widget                                          # type: ignore

from ae.core import DEBUG_LEVEL_DISABLED, DEBUG_LEVEL_ENABLED, sys_platform  # type: ignore
from ae.files import FilesRegister, CachedFile                              # type: ignore
from ae.i18n import default_language, get_f_string, get_text                # type: ignore

# id_of_flow not used here - added for easier import in app project
# noinspection PyUnresolvedReferences
from ae.gui_app import (  # type: ignore
    APP_STATE_SECTION_NAME,
    THEME_LIGHT_BACKGROUND_COLOR, THEME_LIGHT_FONT_COLOR, THEME_DARK_BACKGROUND_COLOR, THEME_DARK_FONT_COLOR,
    MainAppBase, id_of_flow
)  # type: ignore


__version__ = '0.0.30'


kivy.require('1.9.1')  # currently using 1.11.1 but at least 1.9.1 is needed for Window.softinput_mode 'below_target'

# if the entry field is on top of the screen then it will be disappear with below_target mode
# and in the default mode ('') the keyboard will cover the entry field if it is in the lower part of the screen
# therefore commented out the following two code lines (and setting it now depending on the entry field y position)
# if Window:                                  # is None on gitlab ci
#    Window.softinput_mode = 'below_target'   # ensure android keyboard is not covering Popup/text input if at bottom

MAIN_KV_FILE_NAME = 'main.kv'   #: default file name of the main kv file

LOVE_VIBRATE_PATTERN = (0.0, 0.12, 0.12, 0.21, 0.03, 0.12, 0.12, 0.12)
""" short/~1.2s vibrate pattern for fun/love notification. """

ERROR_VIBRATE_PATTERN = (0.0, 0.09, 0.09, 0.18, 0.18, 0.27, 0.18, 0.36, 0.27, 0.45)
""" long/~2s vibrate pattern for error notification. """

CRITICAL_VIBRATE_PATTERN = (0.00, 0.12, 0.12, 0.12, 0.12, 0.12,
                            0.12, 0.24, 0.12, 0.24, 0.12, 0.24,
                            0.12, 0.12, 0.12, 0.12, 0.12, 0.12)
""" very long/~2.4s vibrate pattern for critical error notification (sending SOS to the mobile world;) """


WIDGETS = '''\
#: import Window kivy.core.window.Window

#: import DEBUG_LEVELS ae.core.DEBUG_LEVELS
#: import DEF_LANGUAGE ae.i18n.DEF_LANGUAGE
#: import installed_languages ae.i18n.installed_languages

#: import MIN_FONT_SIZE ae.gui_app.MIN_FONT_SIZE
#: import MAX_FONT_SIZE ae.gui_app.MAX_FONT_SIZE
#: import THEME_LIGHT_BACKGROUND_COLOR ae.gui_app.THEME_LIGHT_BACKGROUND_COLOR
#: import THEME_LIGHT_FONT_COLOR ae.gui_app.THEME_LIGHT_FONT_COLOR
#: import THEME_DARK_BACKGROUND_COLOR ae.gui_app.THEME_DARK_BACKGROUND_COLOR
#: import THEME_DARK_FONT_COLOR ae.gui_app.THEME_DARK_FONT_COLOR

#: import id_of_flow ae.gui_app.id_of_flow
#: import flow_key ae.gui_app.flow_key
#: import flow_key_split ae.gui_app.flow_key_split


<ThemeButton>:
    circle_fill_color: 0, 0, 0, 0
    square_fill_color: 0, 0, 0, 0
    fill_pos: self.fill_pos or self.pos
    fill_size: self.fill_size or self.size
    source: themeButtonImage.source
    size_hint: 1, None
    size_hint_min_x: self.height
    height: app.ae_states['font_size'] * 1.5
    font_size: app.ae_states['font_size']
    color: app.font_color
    canvas.before:
        Color:
            rgba: self.square_fill_color
        RoundedRectangle:
            pos: self.fill_pos or self.pos
            size: self.fill_size or self.size
        Color:
            rgba: self.circle_fill_color
        Ellipse:
            pos: self.fill_pos or self.pos
            size: self.fill_size or self.size
    Image:
        id: themeButtonImage
        source: root.source
        allow_stretch: True
        keep_ratio: False
        opacity: 1 if self.source else 0
        pos: self.parent.fill_pos or self.parent.pos
        size: self.parent.fill_size or self.parent.size


<ThemeInput@TextInput>:
    font_size: app.ae_states['font_size']
    cursor_color: app.font_color
    foreground_color: app.font_color
    background_color: Window.clearcolor


<FlowButton@ThemeButton>:
    ae_flow_id: ''
    ae_clicked_kwargs: dict(popup_kwargs=dict(parent=self))
    ae_icon_name: ""
    on_release: app.main_app.change_flow(self.ae_flow_id, **self.ae_clicked_kwargs)
    source:
        app.main_app.img_file(self.ae_icon_name or flow_key_split(self.ae_flow_id)[0], \
                              app.ae_states['font_size'], app.ae_states['light_theme'])


<OptionalButton@FlowButton>:
    visible: False
    size_hint: None, None
    width: self.height if self.visible else 0
    height: self.height if self.visible else 0
    disabled: not self.visible
    opacity: 1 if self.visible else 0


# DropDown flow gets handled identical like for a Popup
<FlowDropDown>:
    ae_closed_kwargs: dict(flow_id=id_of_flow('', '')) if app.main_app.flow_path_action(-2) in ('', 'enter') else dict()
    on_dismiss: app.main_app.change_flow(id_of_flow('close', 'flow_popup'), **self.ae_closed_kwargs)
    auto_width: False
    width: min(Window.width - sp(90), sp(960))
    canvas.after:
        Color:
            rgba: app.font_color
        Line:
            width: sp(1.8)
            rounded_rectangle: self.x, self.y, self.width, self.height, sp(9)


<FlowPopup>:
    ae_closed_kwargs: dict(flow_id=id_of_flow('', '')) if app.main_app.flow_path_action(-2) in ('', 'enter') else dict()
    on_dismiss: app.main_app.change_flow(id_of_flow('close', 'flow_popup'), **self.ae_closed_kwargs)
    auto_dismiss: True
    separator_color: app.font_color
    title_align: 'center'
    title_size: app.main_app.font_size


<UserPreferencesButton@FlowButton>:
    ae_flow_id: id_of_flow('open', 'user_preferences')
    circle_fill_color: app.mixed_back_ink


<UserPreferencesOpenPopup@FlowDropDown>:
    canvas.before:
        Color:
            rgba: app.mixed_back_ink
        RoundedRectangle:
            pos: self.pos
            size: self.size
    ChangeColorButton:
        color_name: 'flow_id_ink'
    ChangeColorButton:
        color_name: 'flow_path_ink'
    ChangeColorButton:
        color_name: 'selected_item_ink'
    ChangeColorButton:
        color_name: 'unselected_item_ink'
    FontSizeButton:
        # pass
    UserPrefSlider:
        app_state_name: 'sound_volume'
        cursor_image: 'atlas://data/images/defaulttheme/audio-volume-high'
    # UserPrefSlider:    current kivy module vibrator.py does not support amplitudes arg of android api
    #    app_state_name: 'vibrate_amplitude'
    #    cursor_image: app.main_app.img_file('vibrate', app.ae_states['font_size'], app.ae_states['light_theme'])
    BoxLayout:
        size_hint_y: None
        height: app.ae_states['font_size'] * 1.5 if installed_languages else 0
        opacity: 1 if installed_languages else 0
        OptionalButton:
            ae_flow_id: id_of_flow('change', 'lang_code', self.text)
            ae_clicked_kwargs: dict(popups_to_close=(self.parent.parent.parent, ))
            square_fill_color:
                app.ae_states['selected_item_ink'] if app.main_app.lang_code in ('', self.text) else Window.clearcolor
            text: DEF_LANGUAGE
            visible: DEF_LANGUAGE not in installed_languages
        LangCodeButton:
            lang_idx: 0
        LangCodeButton:
            lang_idx: 1
        LangCodeButton:
            lang_idx: 2
        LangCodeButton:
            lang_idx: 3
    BoxLayout:
        size_hint_y: None
        height: app.ae_states['font_size'] * 1.5
        ThemeButton:
            text: "dark"
            on_release: app.main_app.change_flow(id_of_flow('change', 'light_theme'), light_theme=False)
            color: THEME_DARK_FONT_COLOR or self.color
            square_fill_color: THEME_DARK_BACKGROUND_COLOR or self.square_fill_color
        ThemeButton:
            text: "light"
            on_release: app.main_app.change_flow(id_of_flow('change', 'light_theme'), light_theme=True)
            color: THEME_LIGHT_FONT_COLOR or self.color
            square_fill_color: THEME_LIGHT_BACKGROUND_COLOR or self.square_fill_color
    BoxLayout:
        size_hint_y: None
        height: app.ae_states['font_size'] * 1.5 if app.main_app.debug else 0
        opacity: 1 if app.main_app.debug else 0
        DebugLevelButton:
            level_idx: 0
        DebugLevelButton:
            level_idx: 1
        DebugLevelButton:
            level_idx: 2
        DebugLevelButton:
            level_idx: 3
    BoxLayout:
        size_hint_y: None
        height: app.ae_states['font_size'] * 1.5 if app.main_app.debug else 0
        opacity: 1 if app.main_app.debug else 0
        KbdInputModeButton:
            text: 'below_target'
        KbdInputModeButton:
            text: 'pan'
        KbdInputModeButton:
            text: 'scale'
        KbdInputModeButton:
            text: 'resize'
        KbdInputModeButton:
            text: ''
    OptionalButton:
        square_fill_color: Window.clearcolor
        size_hint_x: 1
        text: 'kivy settings'
        visible: app.main_app.debug
        on_release: app.open_settings()


<UserPrefSlider@Slider>:
    app_state_name: ''
    value: app.ae_states.get(self.app_state_name, 1.0)
    on_value: app.main_app.change_app_state(self.app_state_name, self.value)
    min: 0.0
    max: 1.0
    step: 0.03
    size_hint_y: None
    height: app.ae_states['font_size'] * 1.5
    cursor_size: app.ae_states['font_size'] * 1.5, app.ae_states['font_size'] * 1.5
    padding: app.ae_states['font_size'] * 2.4
    value_track: True
    value_track_color: app.font_color
    canvas.before:
        Color:
            rgba: Window.clearcolor
        RoundedRectangle:
            pos: self.pos
            size: self.size


<FontSizeButton@FlowButton>:
    ae_flow_id: id_of_flow('edit', 'font_size')
    ae_clicked_kwargs: dict(popup_kwargs=dict(parent_popup_to_close=self.parent.parent, parent=self))
    square_fill_color: Window.clearcolor


<FontSizeEditPopup>:
    on_select:
        app.main_app.change_flow(id_of_flow('change', 'font_size'), \
        font_size=args[1], popups_to_close=(self.parent_popup_to_close, ))
    FontSizeSelectButton:
        font_size: MIN_FONT_SIZE
    FontSizeSelectButton:
        font_size: MIN_FONT_SIZE + (MAX_FONT_SIZE - MIN_FONT_SIZE) * 1 / 6
    FontSizeSelectButton:
        font_size: MIN_FONT_SIZE + (MAX_FONT_SIZE - MIN_FONT_SIZE) * 2 / 6
    FontSizeSelectButton:
        font_size: (MIN_FONT_SIZE + MAX_FONT_SIZE) / 2
    FontSizeSelectButton:
        font_size: MIN_FONT_SIZE + (MAX_FONT_SIZE - MIN_FONT_SIZE) * 4 / 6
    FontSizeSelectButton:
        font_size: MIN_FONT_SIZE + (MAX_FONT_SIZE - MIN_FONT_SIZE) * 5 / 6
    FontSizeSelectButton:
        font_size: MAX_FONT_SIZE


<FontSizeSelectButton@Button>:
    # text: f'Aa Bb Zz {round(self.font_size)}'  F-STRING displaying always 15 as font size
    text: 'Aa Bb Zz {}'.format(round(self.font_size))
    on_release: self.parent.parent.select(self.font_size)
    size_hint_y: None
    size: self.texture_size
    color: app.font_color
    background_normal: ''
    background_color:
        app.ae_states['selected_item_ink'] if app.main_app.font_size == self.font_size else Window.clearcolor


<ChangeColorButton@FlowButton>:
    color_name: 'flow_id_ink'
    ae_flow_id: id_of_flow('open', 'color_picker', self.color_name)
    ae_clicked_kwargs: dict(popup_kwargs=dict(parent=self))
    square_fill_color: Window.clearcolor
    circle_fill_color: app.ae_states[self.color_name]
    text: self.color_name


<ColorPickerOpenPopup@FlowDropDown>:
    ColorPicker:
        color: app.ae_states[root.attach_to.color_name] if root.attach_to else (0, 0, 0, 0)
        on_color: root.attach_to and app.main_app.change_app_state(root.attach_to.color_name, tuple(args[1]))
        size_hint_y: None
        height: self.width
        canvas.before:
            Color:
                rgba: Window.clearcolor
            RoundedRectangle:
                pos: self.pos
                size: self.size


<LangCodeButton@OptionalButton>:
    lang_idx: 0
    ae_flow_id: id_of_flow('change', 'lang_code', self.text)
    ae_clicked_kwargs: dict(popups_to_close=(self.parent.parent.parent, ))
    square_fill_color: app.ae_states['selected_item_ink'] if app.main_app.lang_code == self.text else Window.clearcolor
    size_hint_x: 1 if self.visible else None
    text: installed_languages[min(self.lang_idx, len(installed_languages) - 1)]
    visible: len(installed_languages) > self.lang_idx


<DebugLevelButton@OptionalButton>:
    level_idx: 0
    ae_flow_id: id_of_flow('change', 'debug_level', self.text)
    ae_clicked_kwargs: dict(popups_to_close=(self.parent.parent.parent, ))
    square_fill_color:
        app.ae_states['selected_item_ink'] if app.main_app.debug_level == self.level_idx else Window.clearcolor
    size_hint_x: 1 if self.visible else None
    text: DEBUG_LEVELS[min(self.level_idx, len(DEBUG_LEVELS) - 1)]
    visible: app.main_app.debug


<KbdInputModeButton@OptionalButton>:
    ae_flow_id: id_of_flow('change', 'kbd_input_mode', self.text)
    ae_clicked_kwargs: dict(popups_to_close=(self.parent.parent.parent, ))
    square_fill_color:
        app.ae_states['selected_item_ink'] if app.main_app.kbd_input_mode == self.text else Window.clearcolor
    size_hint_x: 1 if self.visible else None
    visible: app.main_app.debug


<MessageShowPopup>:
    size_hint: 0.9, None
    height: min(Window.height, err_txt_box.height + self.title_size * 1.8)
    ScrollView:
        Label:
            canvas.before:
                Color:
                    rgba: Window.clearcolor
                RoundedRectangle:
                    pos: self.pos
                    size: self.size
            id: err_txt_box
            text: root.message
            font_size: app.main_app.font_size
            text_size: self.width, None
            size_hint: 1, None
            height: self.texture_size[1]
            color: app.font_color
            Button:     # invisible button for close error popup on error text click
                size: err_txt_box.size
                background_color: 0, 0, 0, 0
                on_release: root.dismiss()

'''
""" helper widgets with integrated app flow and observers ensuring change of app states (e.g. theme and size) """


# class declarations for docs and for to allow initialization of attributes via __init__ kwargs (e.g. ae_closed_kwargs).

class ThemeButton(ButtonBehavior, Label):   # pragma: no cover
    """ theme-able button base class with additional events for double/triple/long touches.

    :Events:
        `on_double_press`:
            Fired with the touch down MotionEvent instance arg when a button get pressed twice within short time.
        `on_triple_press`:
            Fired with the touch down MotionEvent instance arg when a button get pressed three times within short time.
        `on_long_press`:
            Fired with the touch down MotionEvent instance arg when a button get pressed more than 2.4 seconds.

    .. note::
        unit tests are still missing for this widget.

    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.register_event_type('on_double_press')     # pylint: disable=maybe-no-member
        self.register_event_type('on_triple_press')     # pylint: disable=maybe-no-member
        self.register_event_type('on_long_press')       # pylint: disable=maybe-no-member

    def on_touch_down(self, touch: MotionEvent) -> bool:
        """ check for additional events added by this class.

        :param touch:   motion/touch event data.
        :return:        True if event got processed/used.
        """
        if not self.disabled and self.collide_point(touch.x, touch.y):
            is_triple = touch.is_triple_tap
            if is_triple or touch.is_double_tap:
                # pylint: disable=maybe-no-member
                self.dispatch('on_triple_press' if is_triple else 'on_double_press', touch)
                touch.ungrab(self)      # prevent dispatch of on_press
                return True
            # pylint: disable=maybe-no-member
            touch.ud['long_touch_handler'] = long_touch_handler = lambda dt: self.dispatch('on_long_press', touch)
            Clock.schedule_once(long_touch_handler, 2.4)
        return super().on_touch_down(touch)

    @staticmethod
    def _cancel_long_touch_clock(touch):
        long_touch_handler = touch.ud.pop('long_touch_handler', None)
        if long_touch_handler:
            Clock.unschedule(long_touch_handler)    # alternatively: long_touch_handler.cancel()

    def on_touch_move(self, touch: MotionEvent) -> bool:
        """ disable long touch on mouse/finger moves.

        :param touch:   motion/touch event data.
        :return:        True if event got processed/used.
        """
        # alternative method to calculate touch.pos distances is (from tripletap.py):
        # Vector.distance(Vector(ref.sx, ref.sy), Vector(touch.osx, touch.osy)) > 0.009
        if abs(touch.ox - touch.x) > 9 and abs(touch.oy - touch.y) > 9 and self.collide_point(touch.x, touch.y):
            self._cancel_long_touch_clock(touch)
        return super().on_touch_move(touch)

    def on_touch_up(self, touch: MotionEvent) -> bool:
        """ disable long touch on mouse/finger up.

        :param touch:   motion/touch event data.
        :return:        True if event got processed/used.
        """
        if touch.grab_current is self:
            self._cancel_long_touch_clock(touch)
        return super().on_touch_up(touch)

    def on_double_press(self, touch: MotionEvent):
        """ double click default handler

        :param touch:   motion/touch event data with the touched widget in `touch.grab_current`.
        """

    def on_triple_press(self, touch: MotionEvent):
        """ triple click default handler

        :param touch:   motion/touch event data with the touched widget in `touch.grab_current`.
        """

    def on_long_press(self, touch: MotionEvent):
        """ long press default handler

        :param touch:   motion/touch event data with the touched widget in `touch.grab_current`.
        """
        touch.ungrab(self)      # prevent dispatch of on_release


class FlowDropDown(DropDown):
    """ drop down widget used for user selections from a list of items (represented by the children-widgets). """
    ae_closed_kwargs = DictProperty()   #: kwargs passed to all close action flow change event handlers


class FlowPopup(Popup):
    """ pop up widget used for dialogs and other top-most or modal windows. """
    ae_closed_kwargs = DictProperty()   #: kwargs passed to all close action flow change event handlers


class FontSizeEditPopup(FlowDropDown):
    """ drop down to select font size """
    parent_popup_to_close = ObjectProperty()


class FrameworkApp(App):
    """ kivy framework app class proxy redirecting events and callbacks to the main app class instance. """

    landscape = BooleanProperty()                           #: True if app win width is bigger than the app win height
    font_color = ListProperty(THEME_DARK_FONT_COLOR)        #: rgba color of the font used for labels/buttons/...
    mixed_back_ink = ListProperty((.69, .69, .69, 1.))      #: background color mixed from available back inks

    ae_states = DictProperty()                              #: duplicate of MainAppBase app state for events/binds

    def __init__(self, main_app: 'KivyMainApp', **kwargs):
        """ init kivy app """
        self.main_app = main_app                            #: set reference to KivyMainApp instance
        self.title = main_app.app_title                     #: set kivy.app.App.title
        self.icon = os.path.join("img", "app_icon.png")     #: set kivy.app.App.icon

        super().__init__(**kwargs)

        # redirecting class name, app name and directory to the main app class for kv/ini file names is
        # .. no longer needed because main.kv get set in :meth:`KivyMainApp.init_app` and app states
        # .. get stored in the :ref:`ae config files <config-files>`.
        # self.__class__.__name__ = main_app.__class__.__name__
        # self._app_name = main_app.app_name
        # self._app_directory = '.'

    def build(self) -> Widget:
        """ kivy build app callback.

        :return:                root widget (Main instance) of this app.
        """
        Window.bind(on_resize=self.win_pos_size_change,
                    left=self.win_pos_size_change,
                    top=self.win_pos_size_change,
                    on_key_down=self.key_press_from_kivy,
                    on_key_up=self.key_release_from_kivy)

        return Factory.Main()

    def key_press_from_kivy(self, keyboard, key_code, _scan_code, key_text, modifiers) -> bool:
        """ convert and redistribute key down/press events coming from Window.on_key_down.

        :param keyboard:        used keyboard.
        :param key_code:        key code of pressed key.
        :param _scan_code:      key scan code of pressed key.
        :param key_text:        key text of pressed key.
        :param modifiers:       list of modifier keys (including e.g. 'capslock', 'numlock', ...)
        :return:                True if key event got processed used by the app, else False.
        """
        return self.main_app.key_press_from_framework(
            "".join(_.capitalize() for _ in sorted(modifiers) if _ in ('alt', 'ctrl', 'meta', 'shift')),
            keyboard.command_keys.get(key_code) or key_text or str(key_code))

    def key_release_from_kivy(self, keyboard, key_code, _scan_code) -> bool:
        """ key release/up event.

        :return:                return value of call to `on_key_release` (True if ke got processed/used).
        """
        return self.main_app.call_method('on_key_release', keyboard.command_keys.get(key_code, str(key_code)))

    def on_start(self):
        """ kivy app start event, called after :meth:`MainAppBase.run_app` method and MainAppBase.on_app_start event.

        Kivy just created the main layout by calling its :meth:`~kivy.app.App.build` method and
        attached it to the main window.

        Emits the `on_kivy_app_start` event.
       """
        self.main_app.framework_win = self.root.parent
        self.win_pos_size_change()  # init. app./self.landscape (on app startup and after build)
        self.main_app.call_method('on_kivy_app_start')

    def on_pause(self) -> bool:
        """ app pause event automatically saving the app states.

        Emits the `on_app_pause` event.

        :return:                True.
        """
        self.main_app.save_app_states()
        self.main_app.call_method('on_app_pause')
        return True

    def on_resume(self) -> bool:
        """ app resume event automatically loading the app states.

        Emits the `on_app_resume` event.

        :return:                True.
        """
        self.main_app.load_app_states()
        self.main_app.call_method('on_app_resume')
        return True

    def on_stop(self):
        """ quit app event automatically saving the app states.

        Emits the `on_kivy_app_stop` event whereas the method :meth:`MainAppBase.stop_app`
        emits the `on_app_stop` event.
        """
        self.main_app.save_app_states()
        self.main_app.call_method('on_kivy_app_stop')

    def win_pos_size_change(self, *_):
        """ resize handler updates :attr:`~MainAppBase.win_rectangle` app state and :attr:`~FrameworkApp.landscape`. """
        self.main_app.win_pos_size_change(Window.left, Window.top, Window.width, Window.height)


class MessageShowPopup(FlowPopup):
    """ display_error() popup. """
    title = StringProperty(get_text("Error"))
    message = StringProperty()


class _GetTextBinder(Observable):
    """ redirect ae.i18n.get_f_string to an instance of this class.

    kivy currently only support a single one automatic binding in kv files for all function names ending with `_`
    (see `watched_keys` extension in kivy/lang/parser.py line 201; e.g. `f_` would get recognized by the lang_tr
    re pattern, but kivy will only add the `_` symbol to watched_keys and therefore `f_` not gets bound.)
    For to allow both - f-strings and simple get_text messages - this module binds only :func:`ae.i18n.get_f_string`
    to the `get_txt` symbol (instead of :func:`ae.i18n.get_text` to `_` and :func:`ae.i18n.get_f_string` to `f_`).

    :data:`get_txt` can be used as translation callable, but also for to switch the current default language.
    Additionally :data:`get_txt` is implemented as an observer that automatically updates any translations
    messages of all active/visible kv rules on switch of the language at app run-time.

    inspired by (see also discussion at https://github.com/kivy/kivy/issues/1664):
    - https://github.com/tito/kivy-gettext-example
    - https://github.com/Kovak/kivy_i18n_test
    - https://git.bluedynamics.net/phil/woodmaster-trainer/-/blob/master/src/ui/kivy/i18n.py

    """
    observers: List[Tuple[Callable, tuple, dict]] = []
    _bound_uid = -1

    def fbind(self, name: str, func: Callable, *args, **kwargs) -> int:
        """ override fbind (fast bind) from :class:`Observable` for to collect and separate `_` bindings.

        :param name:            attribute name to be bound.
        :param func:            observer notification function (to be called if attribute changes).
        :param args:            args to be passed to the observer.
        :param kwargs:          kwargs to be passed to the observer.
        :return:                unique id of this binding.
        """
        if name == "_":
            self.observers.append((func, args, kwargs))
            # Observable.bound_uid - initialized in _event.pyx/Observable.cinit() - is not available in python:
            # uid = self.bound_uid      # also not available via getattr(self, 'bound_uid')
            # self.bound_uid += 1
            # return uid
            uid = self._bound_uid
            self._bound_uid -= 1
            return uid                  # alternative ugly hack: return -len(self.observers)

        return super().fbind(name, func, *args, **kwargs)

    def funbind(self, name: str, func: Callable, *args, **kwargs):
        """ override fast unbind.

        :param name:            bound attribute name.
        :param func:            observer notification function (called if attribute changed).
        :param args:            args to be passed to the observer.
        :param kwargs:          kwargs to be passed to the observer.
        """
        if name == "_":
            key = (func, args, kwargs)
            if key in self.observers:
                self.observers.remove(key)
        else:
            super().funbind(name, func, *args, **kwargs)

    def switch_lang(self, lang_code: str):
        """ change language and update kv rules properties.

        :param lang_code:       language code to switch this app to.
        """
        default_language(lang_code)

        for func, args, _kwargs in self.observers:
            func(args[0], None, None)

        app = App.get_running_app()
        app.title = get_txt(app.main_app.app_title)

    def __call__(self, text: str, count: Optional[int] = None, language: str = '', **kwargs) -> str:
        """ translate text into the current-default or the passed language.

        :param text:            text to translate.
        :param count:           optional count for pluralization.
        :param language:        language code to translate the passed text to (def=current default language).
        :param kwargs:          extra kwargs.
        :return:                translated text.
        """
        return get_f_string(text, count=count, language=language, **kwargs)


# Sphinx make html is failing if the comment underneath is included (by changing '# ' into '#: ')
get_txt = _GetTextBinder()  # global i18n translation callable and language switcher, rename to `_` in kv file imports


class KivyMainApp(MainAppBase):
    """ Kivy application """
    flow_id_ink: tuple = (0.99, 0.99, 0.69, 0.69)           #: rgba color for flow id / drag&drop node placeholder
    flow_path_ink: tuple = (0.99, 0.99, 0.39, 0.48)         #: rgba color for flow_path/drag&drop item placeholder
    selected_item_ink: tuple = (0.69, 1.0, 0.39, 0.18)      #: rgba color for list items (selected)
    unselected_item_ink: tuple = (0.39, 0.39, 0.39, 0.18)   #: rgba color for list items (unselected)

    kbd_input_mode: str = 'pan'                             #: optional app state for to set Window[Base].softinput_mode

    documents_root_path: str = "."                          #: root file path for app documents, e.g. for import/export

    _debug_enable_clicks: int = 0

    # abstract methods

    def init_app(self, framework_app_class: Type[FrameworkApp] = FrameworkApp
                 ) -> Tuple[Optional[Callable], Optional[Callable]]:
        """ initialize framework app instance and prepare app startup.

        :param framework_app_class:     class to create app instance (optionally extended by app project).
        :return:                        callable for to start and stop/exit the GUI event loop.
        """
        self.documents_root_path = os.path.join(storagepath.get_documents_dir(), self.app_name)

        Builder.load_string(WIDGETS)

        win_rect = self.win_rectangle
        if win_rect:
            Window.left, Window.top = win_rect[:2]
            Window.size = win_rect[2:]

        self.framework_app = framework_app_class(self)
        if os.path.exists(MAIN_KV_FILE_NAME):
            self.framework_app.kv_file = MAIN_KV_FILE_NAME
        self._update_observable_app_states(self.retrieve_app_states())  # copy app states to duplicate DictProperty

        # setup loaded app states within the now available framework app and its widgets
        get_txt.switch_lang(self.lang_code)
        self.change_light_theme(self.light_theme)

        # redirect back ink app state color changes to actualize mixed_back_ink
        setattr(self, 'on_flow_id_ink', self.mix_background_ink)
        setattr(self, 'on_flow_path_ink', self.mix_background_ink)
        setattr(self, 'on_selected_item_ink', self.mix_background_ink)
        setattr(self, 'on_unselected_item_ink', self.mix_background_ink)

        return self.framework_app.run, self.framework_app.stop

    # overwritten and helper methods

    def change_light_theme(self, light_theme: bool):
        """ change font and window clear/background colors to match 'light'/'black' themes.

        :param light_theme:     pass True for light theme, False for black theme.
        """
        Window.clearcolor = THEME_LIGHT_BACKGROUND_COLOR if light_theme else THEME_DARK_BACKGROUND_COLOR
        self.framework_app.font_color = THEME_LIGHT_FONT_COLOR if light_theme else THEME_DARK_FONT_COLOR

    @staticmethod
    def class_by_name(class_name: str) -> Optional[Type]:
        """ resolve kv widgets """
        try:
            return Factory.get(class_name)
        except (FactoryException, AttributeError):
            return None

    def load_sounds(self):
        """ override for to pre-load audio sounds from app folder snd into sound file cache. """
        self.sound_files = FilesRegister('snd', file_class=CachedFile,
                                         object_loader=lambda f: SoundLoader.load(f.path))

    def mix_background_ink(self):
        """ remix background ink if one of the basic back colours change. """
        self.framework_app.mixed_back_ink = (sum(_) / len(_) for _ in zip(
            self.flow_id_ink, self.flow_path_ink, self.selected_item_ink, self.unselected_item_ink))

    def on_flow_widget_focused(self):
        """ set focus to the widget referenced by the current flow id. """
        liw = self.widget_by_flow_id(self.flow_id)
        self.vpo(f"KivyMainApp.on_flow_widget_focused() '{self.flow_id}'"
                 f" {liw} has={getattr(liw, 'focus', 'unsupported') if liw else ''}")
        if liw and getattr(liw, 'is_focusable', False) and not liw.focus:
            liw.focus = True

    def on_kbd_input_mode_change(self, mode: str, _event_kwargs: dict) -> bool:
        """ language app state change event handler.

        :param mode:            the new softinput_mode string (passed as flow key).
        :param _event_kwargs:   unused event kwargs.
        :return:                True for to confirm the language change.
        """
        self.vpo(f"MainAppBase.on_kbd_input_mode_change to {mode}")
        self.change_app_state('kbd_input_mode', mode)
        self.set_var('kbd_input_mode', mode, section=APP_STATE_SECTION_NAME)  # add optional app state var to config
        return True

    def on_lang_code(self):
        """ language code app-state-change-event-handler for to refresh kv rules. """
        self.vpo(f"KivyMainApp.on_lang_code: language got changed to {self.lang_code}")
        get_txt.switch_lang(self.lang_code)

    def on_light_theme(self):
        """ theme app-state-change-event-handler. """
        self.vpo(f"KivyMainApp.on_light_theme: theme got changed to {self.light_theme}")
        self.change_light_theme(self.light_theme)

    def on_user_preferences_open(self, _flow_id: str, _event_kwargs) -> bool:
        """ enable debug mode after clicking 3 times within 6 seconds.

        :param _flow_id:        new flow id.
        :param _event_kwargs:   optional event kwargs; the optional item with the key `popup_kwargs`
                                will be passed onto the `__init__` method of the found Popup class.
        :return:                False for :meth:`~.on_flow_change` get called, opening user preferences popup.

        """
        def _timeout_reset(_dt: float):
            self._debug_enable_clicks = 0

        if self.debug_level == DEBUG_LEVEL_DISABLED:
            self._debug_enable_clicks += 1
            if self._debug_enable_clicks >= 3:
                self.debug_level: int = DEBUG_LEVEL_ENABLED
                self._debug_enable_clicks = 0
            elif self._debug_enable_clicks == 1:
                Clock.schedule_once(_timeout_reset, 6.0)

        return False

    def play_beep(self):
        """ make a short beep sound. """
        self.play_sound('error')

    def play_sound(self, sound_name: str):
        """ play audio/sound file. """
        self.vpo(f"KivyMainApp.play_sound {sound_name}")
        file: Optional[CachedFile] = self.find_sound(sound_name)
        if file:
            try:
                sound_obj = file.loaded_object
                sound_obj.pitch = file.properties.get('pitch', 1.0)
                sound_obj.volume = (
                    file.properties.get('volume', 1.0) * self.framework_app.ae_states.get('sound_volume', 1.))
                sound_obj.play()
            except Exception as ex:
                self.po(f"KivyMainApp.play_sound exception {ex}")
        else:
            self.dpo(f"KivyMainApp.play_sound({sound_name}) not found")

    def play_vibrate(self, pattern: Tuple = (0.03, 0.3)):
        """ play vibrate pattern. """
        self.vpo(f"KivyMainApp.play_vibrate {pattern}")
        try:        # added because is crashing with current plyer version (master should work)
            vibrator.pattern(pattern)
        # except jnius.jnius.JavaException as ex:
        #    self.po(f"KivyMainApp.play_vibrate JavaException {ex}, update plyer to git/master")
        except Exception as ex:
            self.po(f"KivyMainApp.play_vibrate exception {ex}")

    def prevent_keyboard_covering(self, input_box_bottom: float) -> bool:
        """ prevent that the virtual keyboard popping up on mobile platforms is covering the text input field.

        :param input_box_bottom:    y position of the bottom of the input field box.
        :return:                    True if keyboard is covering the passed y/bottom position, else False.
        """
        if sys_platform() != 'android':
            return False

        keyboard_height = Window.keyboard_height or Window.height / 2  # 'or'-fallback because SDL2 reports 0 kbd height
        mode_changed = input_box_bottom < keyboard_height
        Window.softinput_mode = self.kbd_input_mode if mode_changed else ''

        return mode_changed

    def show_message(self, message: str, title: str = "", is_error: bool = True):
        """ display (error) message popup to the user.

        :param message:         message string to display.
        :param title:           title of message box.
        :param is_error:        pass False to not emit error tone/vibration.
        """
        if is_error:
            self.play_vibrate(ERROR_VIBRATE_PATTERN)
            self.play_beep()

        popup_kwargs = dict(message=message)
        if title:
            popup_kwargs['title'] = title

        self.change_flow(id_of_flow('show', 'message'), popup_kwargs=popup_kwargs)

    def show_popup(self, popup_class: Type[Union[Popup, DropDown]], **popup_attributes) -> Widget:
        """ open Popup or DropDown using the `open` method. Overwriting the main app class method.

        :param popup_class:         class of the Popup or DropDown widget.
        :param popup_attributes:    args for to be set as attributes of the popup class instance plus an optional
                                    `parent` kwarg that will be passed as the popup parent widget arg
                                    to the popup.open method; if parent does not get passed then the root widget/layout
                                    of self.framework_app will passed into the popup.open method as the widget argument.
        :return:                    created and displayed/opened popup class instance.
        """
        self.dpo(f"KivyAppBase.show_popup {popup_class} {popup_attributes}")

        # framework_win has absolute screen coordinates and lacks x, y properties, therefore use app.root as def parent
        parent = popup_attributes.pop('parent', self.framework_app.root)
        popup_instance = popup_class(**popup_attributes)
        if self.prevent_keyboard_covering(popup_instance.y):
            container = getattr(popup_instance, '_container', None)
            if container:
                container.clear_widgets()                       # clear container for Popup only
            popup_instance = popup_class(**popup_attributes)    # new instance if kbd covering popup

        if not hasattr(popup_instance, 'close') and hasattr(popup_instance, 'dismiss'):
            popup_instance.close = popup_instance.dismiss       # create close() method alias for DropDown.dismiss()

        popup_instance.open(parent)

        return popup_instance
