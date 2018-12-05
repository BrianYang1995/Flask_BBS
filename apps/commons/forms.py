from wtforms import Form, StringField
from wtforms.validators import Length, Regexp, InputRequired, ValidationError
import hashlib


class MSMCaptchaForm(Form):
    salt = 'jfla&klga#lav%78^hfak83u89t3fa3i&j389'
    telephone = StringField(validators=[Regexp(r'1[345789]\d{9}')])
    timestamp = StringField(validators=[Regexp(r'\d{13}')])
    sign = StringField(validators=[InputRequired()])

    def validate(self):
        result = super(MSMCaptchaForm, self).validate()
        if not result:
            return False

        telephone = self.telephone.data
        timestamp = self.timestamp.data
        sign = self.sign.data
        hash_sign = hashlib.md5((telephone+self.salt+timestamp).encode()).hexdigest()
        if sign != hash_sign:
            return False
        else:
            return True
