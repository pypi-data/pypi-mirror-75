import os
import multiprocessing as mp
import io
import spacy
import pprint
from spacy.matcher import Matcher
from . import reshelper


class ResumeFeatures(object):

    def __init__(
        self,
        resume,
        skills_file=None,
        custom_regex=None
    ):
        nlp = spacy.load('en_core_web_sm')

        custom_nlp = spacy.load(os.path.dirname(os.path.abspath(__file__)))

        self.__custom_regex = custom_regex
        self.__matcher = Matcher(nlp.vocab)
        self.__details = {
            'name': None,
            'email': None,
            'mobile_number': None,
            'skills': None,
            'experience': None,
            'education': None,
            'summary': None,

        }
        self.__resume = resume
        if not isinstance(self.__resume, io.BytesIO):
            ext = os.path.splitext(self.__resume)[1].split('.')[1]
        else:
            ext = self.__resume.name.split('.')[1]
        self.__text_raw = reshelper.extract_text(self.__resume, '.' + ext)
        self.__text = ' '.join(self.__text_raw.split())
        self.__nlp = nlp(self.__text)
        self.__custom_nlp = custom_nlp(self.__text_raw)
        self.__noun_chunks = list(self.__nlp.noun_chunks)
        self.__get_basic_details()

    def get_extracted_data(self):
        return self.__details

    def __get_basic_details(self):
        cust_ent = reshelper.extract_entities_wih_custom_model(
                            self.__custom_nlp
                        )
        name = reshelper.extract_name(self.__nlp, matcher=self.__matcher)
        email = reshelper.extract_email(self.__text)
        mobile = reshelper.extract_mobile_number(self.__text, self.__custom_regex)
        
        # extract name
        
        self.__details['name'] = name

        # extract email
        self.__details['email'] = email

        # extract mobile number
        self.__details['mobile_number'] = mobile

        # extract skills
        try:
            self.__details['skills'] = cust_ent['Skills']
        except KeyError:
            pass


        # extract education 
        try:
            self.__details['education'] = cust_ent['Education']
        except KeyError:
            pass

        # extract summary
        try:
            self.__details['summary'] = cust_ent['Summary']
        except KeyError:
            pass

        # extract experience
        try:
            self.__details['experience'] = cust_ent['Experience']
        except KeyError:
            pass

        return


def resume_result_wrapper(resume):
    parser = ResumeFeatures(resume)
    return parser.get_extracted_data()


if __name__ == '__main__':
    pool = mp.Pool(mp.cpu_count())

    resumes = []
    data = []
    for root, directories, filenames in os.walk('resumes/'):
        for filename in filenames:
            file = os.path.join(root, filename)
            resumes.append(file)

    results = [
        pool.apply_async(
            resume_result_wrapper,
            args=(x,)
        ) for x in resumes
    ]

    results = [p.get() for p in results]

    pprint.pprint(results)
