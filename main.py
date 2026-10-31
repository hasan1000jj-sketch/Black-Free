# X Black - Android-friendly Python app (Kivy)
# Safe report organizer: records evidence and opens TikTok profile/reporting page.
from kivy.app import App
from kivy.lang import Builder
from kivy.core.clipboard import Clipboard
from kivy.utils import platform
from kivy.metrics import dp
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from datetime import datetime
import json, os, webbrowser

KV = r'''
#:import dp kivy.metrics.dp
BoxLayout:
    orientation: 'vertical'
    padding: dp(16)
    spacing: dp(10)
    canvas.before:
        Color:
            rgba: (0.94, 0.96, 0.98, 1)
        Rectangle:
            pos: self.pos
            size: self.size
    Label:
        text: '[b]X BLACK[/b]\nمساعد تنظيم البلاغات الرسمية'
        markup: True
        font_size: '23sp'
        color: (0.08,0.12,0.19,1)
        size_hint_y: None
        height: dp(78)
    Label:
        text: 'اسم المستخدم في تيك توك'
        color: (0.1,0.1,0.1,1)
        size_hint_y: None
        height: dp(28)
    TextInput:
        id: username
        hint_text: 'مثال: username بدون @'
        multiline: False
        size_hint_y: None
        height: dp(48)
    Label:
        text: 'نوع المخالفة المشتبه بها'
        color: (0.1,0.1,0.1,1)
        size_hint_y: None
        height: dp(28)
    Spinner:
        id: reason
        text: 'اختر نوع المخالفة'
        values: ['انتحال شخصية','احتيال أو تضليل','مضايقة أو تنمر','محتوى عنيف','محتوى آخر']
        size_hint_y: None
        height: dp(48)
    Label:
        text: 'ملاحظات / وصف الأدلة'
        color: (0.1,0.1,0.1,1)
        size_hint_y: None
        height: dp(28)
    TextInput:
        id: notes
        hint_text: 'اكتب وصفاً مختصراً ودقيقاً للمخالفة وروابط الأدلة إن وجدت'
        multiline: True
    Button:
        text: 'حفظ سجل البلاغ على الهاتف'
        size_hint_y: None
        height: dp(50)
        background_normal: ''
        background_color: (0.12,0.34,0.55,1)
        on_release: app.save_report()
    Button:
        text: 'فتح ملف الحساب في تيك توك'
        size_hint_y: None
        height: dp(48)
        on_release: app.open_profile()
    Button:
        text: 'عرض طريقة الإبلاغ الرسمية'
        size_hint_y: None
        height: dp(48)
        on_release: app.show_guide()
    Label:
        id: status
        text: 'يحفظ التطبيق بياناتك محلياً فقط ولا يرسل بلاغات تلقائية.'
        color: (0.22,0.25,0.29,1)
        font_size: '13sp'
        size_hint_y: None
        height: dp(45)
'''

class XBlackApp(App):
    def build(self):
        self.title = 'X Black'
        self.data_file = os.path.join(self.user_data_dir, 'reports.json')
        return Builder.load_string(KV)

    def popup(self, title, message):
        Popup(title=title, content=Label(text=message), size_hint=(.88,.48)).open()

    def save_report(self):
        u = self.root.ids.username.text.strip().lstrip('@')
        reason = self.root.ids.reason.text
        notes = self.root.ids.notes.text.strip()
        if not u or reason == 'اختر نوع المخالفة':
            self.popup('تنبيه', 'أدخل اسم المستخدم واختر نوع المخالفة أولاً.')
            return
        record = {'username': u, 'reason': reason, 'notes': notes,
                  'created_at': datetime.now().isoformat(timespec='seconds'),
                  'status': 'بانتظار تقديم البلاغ يدوياً'}
        try:
            records = []
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    records = json.load(f)
            records.append(record)
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(records, f, ensure_ascii=False, indent=2)
            self.root.ids.status.text = 'تم حفظ السجل على الهاتف بنجاح.'
            self.popup('تم الحفظ', 'حُفظ سجل البلاغ محلياً. راجع الأدلة قبل تقديم بلاغ واحد دقيق.')
        except Exception as e:
            self.popup('خطأ', 'تعذر حفظ السجل: ' + str(e))

    def open_profile(self):
        u = self.root.ids.username.text.strip().lstrip('@')
        if not u:
            self.popup('تنبيه', 'اكتب اسم المستخدم أولاً.')
            return
        webbrowser.open('https://www.tiktok.com/@' + u)

    def show_guide(self):
        self.popup('الإبلاغ الرسمي', 'افتح الحساب في تيك توك، ثم القائمة أو زر المشاركة، واختر إبلاغ (Report). حدّد السبب المطابق، وأرفق الأدلة الحقيقية. لا تقدّم بلاغاً إذا لم توجد مخالفة.')

if __name__ == '__main__':
    XBlackApp().run()
