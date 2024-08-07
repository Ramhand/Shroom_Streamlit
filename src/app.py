import pandas as pd
import streamlit as st
import regex as re
from ucimlrepo import fetch_ucirepo
import pickle


class RazzleDazzle:
    with open('../models/fun_guy.dat', 'rb') as file:
        model = pickle.load(file)
    data = fetch_ucirepo(id=73)
    data = pd.concat([pd.DataFrame(data.data.features), pd.DataFrame(data.data.targets)], axis=1)
    data = data[['odor', 'gill-attachment', 'gill-size', 'stalk-surface-below-ring', 'stalk-color-above-ring',
           'spore-print-color', 'population']]
    key = {'odor': {'almond': 2, 'anise': 3, 'creosote': 6, 'fishy': 7, 'foul': 5, 'musty': 9, 'none': 4, 'pungent': 1, 'spicy': 8}, 'gill-attachment': {'attached': 1, 'descending': 2}, 'gill-size': {'broad': 2, 'narrow': 1}, 'stalk-surface-below-ring': {'fibrous': 2, 'scaly': 3, 'silky': 4, 'smooth': 1}, 'stalk-color-above-ring': {'brown': 4, 'buff': 5, 'cinnamon': 8, 'gray': 2, 'orange': 7, 'pink': 3, 'red': 6, 'white': 1, 'yellow': 9}, 'spore-print-color': {'black': 1, 'brown': 2, 'buff': 9, 'chocolate': 4, 'green': 6, 'orange': 7, 'purple': 3, 'white': 5, 'yellow': 8}, 'population': {'abundant': 3, 'clustered': 6, 'numerous': 2, 'scattered': 1, 'several': 4, 'solitary': 5}}

    def __init__(self):
        self.autogeny()

    def autogeny(self):
        self.title = st.title('Can you eat it?', )
        self.header = st.header('Mushroom Identification')
        self.form, self.combo_box = text_chunker(self)
        self.answer = st.write('')

    def jazzhands(self):
        dic = {k:v[self.combo_box[k].lower()] for k, v in self.key.items()}
        df = pd.DataFrame(dic, index=[0])
        answer = self.model.predict(df)[0]
        if answer == 1:
            self.answer = st.write('While I cannot stress enough that you should not eat wild mushrooms without serious training in identification, the model says it is edible.')
        else:
            self.answer = st.write('Drop it.  No seriously, do not eat that.  Perhaps there are some berries nearby?')




def text_chunker(razdaz):
    dic = {'odor': 'What does it smell like?',
           'gill-attachment': 'How are the gills attached under the cap?',
           'gill-size': 'How large are said gills?',
           'stalk-surface-below-ring': 'What is the texture of the stalk underneath the ring?',
           'stalk-color-above-ring': 'What color is the stalk above the ring?',
           'spore-print-color': 'What color spore print does the mushroom leave?',
           'population': 'What is the population of this particular mushroom like in the area in which it was found?'}
    cb = {}
    with st.form('input') as form:
        for k, v in razdaz.key.items():
            cb[k] = st.selectbox(label=dic[k], options=[i.title() for i in v.keys()])
        st.form_submit_button(on_click=razdaz.jazzhands)
        return form, cb



if __name__ == '__main__':
    RazzleDazzle()
