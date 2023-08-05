import pandas as pd
import os
import re

from split_datalawyer.sentences.split_utils import split_by_sentence, split_by_break

__DEFAULT_STOP_PHRASES__ = 'stoppatterns.txt'
__sentence_split_version__ = "1.4"
__ENDING_PUNCTUATION_TUPLE__ = tuple([".", ";", ":", "\"", "!", "?", ")"])

class SentenceSplit():

    def __init__(self, stop_patterns_path=__DEFAULT_STOP_PHRASES__, debug_log=False):

        self._list_stop_patterns = self._get_stop_patterns(stop_patterns_path)
        self._list_abbreviations = self._get_abbreviations()
        self._debug_log = debug_log
        self._debug_messages = []

    def _log(self, message):
        if self._debug_log:
            self._debug_messages.append(message)
    
    def generate_log(self): 
        if self._debug_log:
            with open("sentence_split_log.txt", mode='w', encoding='utf8') as log_file:
                for message in self._debug_messages:
                    log_file.write(message + "\n")

    def _get_abbreviations(self):
        abbreviations_path = os.path.join(self._get_local_directory(), "lista_abreviacoes.csv")
        f = open(abbreviations_path, "r", encoding='utf-8')
        abbreviations = f.readlines()
        f.close()

        return [x.replace("\n", "") + "." for x in abbreviations]
    
    def _get_local_directory(self):
        abspath = os.path.abspath(__file__)
        dname = os.path.dirname(abspath)

        return dname

    def _get_stop_patterns(self, stop_patterns_path):
        if stop_patterns_path == __DEFAULT_STOP_PHRASES__:
            stop_patterns_path = os.path.join(self._get_local_directory(), stop_patterns_path)

        f = open(stop_patterns_path, encoding='utf-8')
        phrase_list = f.readlines()
        f.close()

        return [re.compile(x.replace("\n", "")) for x in phrase_list]
    
    def _parenthesis_is_closed(self, phrase):
        if phrase != "":
            if phrase.count("(") > phrase.count(")"):
                return False

        return True
    
    def _concat_inverted_phrases(self, df):
        df = df[df['final_text'] != ""]
        df = df.sort_values('index').reset_index(drop=True)

        for i in range(1, len(df['final_text'])):
            previous_text = df['final_text'][i-1]
            current_text = df['final_text'][i]

            if current_text != "":            
                if i+1 < len(df['final_text']):
                    next_text = df['final_text'][i+1]            
                    
                    previous_has_end = previous_text.endswith(__ENDING_PUNCTUATION_TUPLE__)
                    current_text_starts_lower = current_text[0].islower()
                    current_text_has_end = current_text.endswith(__ENDING_PUNCTUATION_TUPLE__)
                    next_has_not_end = not next_text.endswith(__ENDING_PUNCTUATION_TUPLE__)

                    if current_text_starts_lower and current_text_has_end and previous_has_end and next_has_not_end:
                        df['final_text'][i+1] =  next_text + " " + current_text
                        df['final_text'][i] = ""
                        self._log("_concat_inverted_phrases: " + next_text + " " + current_text)

        return df


    def _concat_broken_phrases(self, df):        
        continuation_terms = ["no", "na", "nos", "nas", "de", "do", "da", "dos", "das", ","]
        df['final_text'] = df['text']

        for i in range(len(df['final_text'])):
            current_text = df['final_text'][i].strip()
            text_not_empty = current_text != ""
            end_with_punctuation = current_text.endswith(__ENDING_PUNCTUATION_TUPLE__)            
            all_text_upper = text_not_empty and current_text.isupper() and len(current_text) > 1
            parenthesis_not_closed = not self._parenthesis_is_closed(current_text)
            search_phrase_continuation = text_not_empty and (not end_with_punctuation) and (not all_text_upper) or parenthesis_not_closed
            phrase_has_continuation = False

            if search_phrase_continuation:
                phrases_parts_index = []
                previous_phrase_index = 1
                waiting_close_parenthesis = parenthesis_not_closed

                for j in range(i+1, len(df['final_text'])):
                    next_text = df['final_text'][j]
                    next_text_was_duplicated = bool(df['duplicated'][j])

                    if(next_text_was_duplicated):
                        self._log("_concat_broken_phrases: next_text_was_duplicated: " + next_text)                        

                    if next_text != "" and (not next_text_was_duplicated):
                        previous_text = ""
                        if j-previous_phrase_index >= 0: 
                            previous_text = df['final_text'][j-previous_phrase_index]                        

                        previous_ends_with_continuation = previous_text != "" and (previous_text.split()[-1] in continuation_terms)

                        if not waiting_close_parenthesis:                            
                            waiting_close_parenthesis = not self._parenthesis_is_closed(next_text)

                        if next_text.split()[0].islower() or previous_ends_with_continuation or (waiting_close_parenthesis):
                            phrases_parts_index.append(j)                            
                            next_text_end_not_with_abbreviation = not next_text.split()[-1] in self._list_abbreviations

                            if next_text.endswith(__ENDING_PUNCTUATION_TUPLE__) and next_text_end_not_with_abbreviation and not waiting_close_parenthesis:
                                self._log("waiting_close_parenthesis: " + df['final_text'][j])

                            if waiting_close_parenthesis:
                                waiting_close_parenthesis = not (next_text.count(")") > next_text.count("("))

                            if next_text.endswith(__ENDING_PUNCTUATION_TUPLE__) and next_text_end_not_with_abbreviation and (not waiting_close_parenthesis):
                                phrase_has_continuation = True
                                break
                        else:
                            if len(phrases_parts_index) > 0:
                                self._log("_concat_broken_phrases: ignored_parts: ["+ "| ".join([df['final_text'][index] for index in phrases_parts_index]) +"] next_text: " + next_text)
                            break
                    else:
                        previous_phrase_index = previous_phrase_index+1


                end_of_phrase = ""
                if phrase_has_continuation:                    
                    for part_index in phrases_parts_index:
                        phrase_part = df['final_text'][part_index]
                        end_of_phrase = end_of_phrase + " " + phrase_part
                        df['final_text'][part_index] = ""

                    if end_of_phrase != "":
                        df['final_text'][i] = current_text + " " + end_of_phrase.strip()

        return df

    def _remove_small_phrases(self, df, minimium_word_count=3):
        if minimium_word_count > 0:
            df['final_text'] = df['text']

            for i in range(len(df['final_text'])):        
                phrase_is_small = len(df['final_text'][i].split()) < minimium_word_count
                
                if phrase_is_small:
                    df['final_text'][i] = ""
                
        return df        
    
    def _remove_duplicates(self, df, remove_stop_phrases):
        df = df[df['text'] != ""]       
        df['duplicated'] = df['text'].duplicated(False) 
        df = df.sort_values(['text', 'index']).reset_index(drop=True)
        duplicated_phrases = list(df[df['duplicated']]['text'])        
        self._log("_remove_duplicates: duplicated_phrases: [" + '| '.join(duplicated_phrases) + "]")

        previous_value = ""
        phrases_count = len(df['text'])
        for i in range(phrases_count):
            reserve_index = phrases_count-i-1
            current_value = df['text'][reserve_index]            

            both_equals = previous_value == current_value
            is_number_page = current_value.isdigit()
            if is_number_page:
                self._log("is_number_page: " + current_value)

            is_stop_phrase =remove_stop_phrases and any(regex.match(current_value) for regex in self._list_stop_patterns)
            if is_stop_phrase:
                debug_stop=True

            remove_text = both_equals or is_number_page or is_stop_phrase            

            if(remove_text):
                df['text'][reserve_index] = ""

            if (df['text'][reserve_index] != ""):
                previous_value = df['text'][reserve_index]

        df = df[df['text'] != ""]
        df = df.sort_values('index').reset_index(drop=True)

        return df

    def _split_by_punctuation(self, df):            
        column_name = 'text'

        if "final_text" in df.columns:
            column_name = 'final_text'

        df = df[df[column_name] != ""]

        phrase_list = []
        for texto in list(df[column_name]):            
            phrases = split_by_sentence(texto, True)
            phrase_list.extend(phrases)

        temp_object_list = [{'index': index, 'text': phrase_list[index]}
                            for index in range(len(phrase_list))]
                            
        df_splited = pd.DataFrame(temp_object_list)
        
        return df_splited
    
    def get_sentences(self, text, remove_duplicated=True, concat_phrases=True, concat_inverted_phrases=True, remove_stop_phrases=True, minimium_word_count=0):
        df = self.get_sentences_with_index(text,
                                           remove_duplicated=remove_duplicated,
                                           concat_phrases=concat_phrases,
                                           concat_inverted_phrases=concat_inverted_phrases, 
                                           remove_stop_phrases=remove_stop_phrases, 
                                           minimium_word_count=minimium_word_count)
        
        if df is not None:
            column_name = 'text'

            if "final_text" in df.columns:
                column_name = 'final_text'

            df = df[df[column_name] != ""]
            sentences = list(df[column_name])

            return sentences
        
        return []

    def get_sentences_with_index(self, text, remove_duplicated=True, concat_phrases=True, concat_inverted_phrases=True, remove_stop_phrases=True, minimium_word_count=0):

        sentence_list = split_by_break(text)
        temp_object_list = [{'index': index, 'text': sentence_list[index]}
                            for index in range(len(sentence_list))]

        df = pd.DataFrame(temp_object_list)
        
        if remove_duplicated:
            df = self._remove_duplicates(df, remove_stop_phrases)
        
        if concat_phrases:
            df = self._concat_broken_phrases(df)        
        
            if concat_inverted_phrases:
                df = self._concat_inverted_phrases(df)     

        df = self._split_by_punctuation(df)

        if minimium_word_count > 0:
            df = self._remove_small_phrases(df, minimium_word_count)

        if not df.empty:
            df = df[df['text'] != ""]
            df = df.sort_values('index').reset_index(drop=True)
            df['index'] = df.index

            return df
        
        return None