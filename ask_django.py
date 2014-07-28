from pyke import qa_helpers
from django import forms
from django.utils.safestring import SafeString
import itertools

class DjangoAsyncInterrupt(Exception):
    pass

class DjangoAskModule(object):
    def __init__(self, engine, session, *args, **kwargs):
        self.engine = engine
        self.session = session
        self.form = None

    def ask_yn(self, question, format_params):
        return self.ask_question(question, format_params)

    def ask_integer(self, question, format_params):
        return self.ask_question(question, format_params)

    def ask_float(self, question, format_params):
        return self.ask_question(question, format_params)

    def ask_number(self, question, format_params):
        return self.ask_question(question, format_params)

    def ask_string(self, question, format_params):
        return self.ask_question(question, format_params)

    def ask_select_1(self, question, format_params):
        return self.ask_question(question, format_params)

    def ask_select_n(self, question, format_params):
        return self.ask_question(question, format_params)

    def ask_question(self, question, format_params):
        self.form = None

        stored_q = {}
        stored_q["base"] = question.knowledge_base.name 
        stored_q["name"] = question.name
        stored_q["format_params"] = format_params
        self.session["last_question"] = stored_q

        raise DjangoAsyncInterrupt() 

    def question_key(self, question, type):
        return "%s:%%:%s" % (question, type)

    def record_answer(self, postdata):
        q = self.session["last_question"]
        params = q["format_params"]
        question = self.engine.get_ke(q["base"], q["name"])
        q_type = question.user_question.__class__.__name__

        FormType = self.getFormType()
        self.form = FormType(postdata)
        if not self.form.is_valid():
            return False
        answer = self.form.cleaned_data["question"]
  
        alternatives = None

        if q_type == "yn":
            pass
        elif q_type == "integer":
            pass
        elif q_type == "float":
            pass
        elif q_type == "number":
            if answer.to_integral() == answer:
                answer = int(answer)
            else:
                answer = float(answer)
        elif q_type == "string":
            pass
        elif q_type == "select_1":
            alternatives = question.prepare_arg2(params)
            for alt in alternatives:
                (tag, desc) = alt
                try:
                    int_ans = int(answer)
                except ValueError:
                    int_ans = None
                if tag == int_ans:
                    answer = tag
                    break
                if tag == answer:
                    break
        elif q_type == "select_n":
            alternatives = question.prepare_arg2(params)
            mapped_answers = []
            for alt in alternatives:
                for ans in answer:
                    (tag, desc) = alt
                    try:
                        int_ans = int(ans)
                    except ValueError:
                        int_ans = None
                    if tag == int_ans:
                        mapped_answers.append(tag)
                        break
                    if tag == ans:
                        mapped_answers.append(tag)
            answer = mapped_answers
        else:
            raise Exception("Unrecognised type: %s" % q_type)

        if alternatives:
            match = None
        else:
            match = question.prepare_arg2(params)

        if match:
            try:
                qa_helpers.match(answer, match)
            except ValueError, e:
                self.form._errors["question"] = self.form.error_class([
                            "Answer should be %s. Got %s" % (
                            e.message, repr(answer))])
                return False

        question.record_answer(params, answer)

        reviews = question.prepare_review(params)
        if reviews:
            def matches2(ans, test):
                try:
                    qa_helpers.match(ans, test)
                    return True
                except ValueError:
                    return False

            def matches(ans, test):
                if isinstance(ans, (tuple,list)):
                    return any(itertools.imap(
                            lambda elem: matches2(elem, test), ans))
                return matches2(ans, test)

            self.session["last_review"] = SafeString(u"</p><p>".join(
                        review_str for review_test, review_str in reviews
                                    if matches(answer, review_test)))
                            
        return True

    def getForm(self):
        if self.form:
            return self.form
        else:
            return self.getFormType()()

    def getFormType(self):
        q = self.session["last_question"]
        params = q["format_params"]
        question = self.engine.get_ke(q["base"], q["name"])
        q_type = question.user_question.__class__.__name__
        question_text = question.prepare_question(params)

        fields = {}
        if q_type == "yn":
            fields["question"] = forms.BooleanField(required=False,
                                        label=question_text)
        elif q_type == "integer":
            fields["question"] = forms.IntegerField(required=True,
                                        label=question_text)
        elif q_type == "float":
            fields["question"] = forms.FloatField(required=False,
                                        label=question_text)
        elif q_type == "number":
            fields["question"] = forms.DecimalField(required=False,
                                        label=question_text)
        elif q_type == "string":
            fields["question"] = forms.CharField(required=False,
                                        label=question_text)
        elif q_type == "select_1":
            alternatives = question.prepare_arg2(params)
            choices = []
            for alternative in alternatives:
                choices.append(alternative)
            fields["question"] = forms.ChoiceField(required=False,
                                        label=question_text,
                                        choices=choices)
        elif q_type == "select_n":
            alternatives = question.prepare_arg2(params)
            choices = []
            for alternative in alternatives:
                choices.append(alternative)
            fields["question"] = forms.MultipleChoiceField(required=False,
                                        label=question_text,
                                        choices=choices)
        else:
            raise Exception("Unrecognised type: %s" % q["type"])

        return type("QuestionForm", (forms.BaseForm,), {
                        "base_fields": fields
                        })

