#include <bits/stdc++.h>
#include <set>
#include <cstdint>
#include <algorithm>
#include <vector>
#include <fstream>
using namespace std;

set<string> GlobalPerms;

void permute(string str, const string& out){
    if (str.empty()){
        GlobalPerms.insert(out);
        return;
    }

    for (int i = 0; i < str.size(); i++){
        permute(str.substr(1), out + str[0]);
        rotate(str.begin(), str.begin() + 1, str.end());
    }
}

bool set_contains(const set<string>& s, const string& st){
    return s.find(st) != s.end();
}

int main(){

    set<string> dictionary;

    ifstream dic_file("words.txt");
    string dic_word;
    while (getline(dic_file, dic_word)){
        transform(dic_word.begin(), dic_word.end(), dic_word.begin(), ::tolower);
        dictionary.insert(dic_word);
    }
    dic_file.close();

    /// Mickey Mouse, takes long time. Removed from list.

    vector<string> tested_sentences = {"i love you",
                                       "ce rulez",
                                       "turgut uyar",
                                       "ubuntu",
                                       "zzzz",
                                       "hayat zor"};

    ofstream test_file("part3.yaml", ios::out | ios::trunc);

    string init_string = "- init:\n"
                         "    run: rm -f part3 part3.o part3.hi\n"
                         "    visible: false\n"
                         "- compile:\n"
                         "    run: ghc part3.hs -o part3\n"
                         "    blocker: true\n";

    string close_string = "- cleanup:\n"
                          "    run: rm -f part3 part3.o part3.hi\n"
                          "    visible: false\n";

    test_file << init_string;

    for (int ind = 0; ind < tested_sentences.size(); ind++){

        string sentence = tested_sentences[ind];

        test_file << "- case_" + to_string(ind+1) + ":\n"
                     "    run: ./part3 \"" + sentence +"\"\n"
                     "    script:\n";

        string original_sentence = sentence;
        string::iterator end_pos = remove(sentence.begin(), sentence.end(), ' ');
        sentence.erase(end_pos, sentence.end());

        uint8_t binary_spacer_bit_count = sentence.size() - 1;
        uint32_t binary_spacer_max = (1u << (sentence.size() - 1));
        permute(sentence, "");

        //cout << GlobalPerms.size() << endl;

        vector<vector<string>> possible_sentences;
        uint32_t binary_spacer;

        for (string const& st : GlobalPerms){
            for(binary_spacer = 0; binary_spacer < binary_spacer_max; binary_spacer++){
                bool failed = false;
                vector<string> seperated_words;
                string current_st = st.substr(0, 1);
                for(uint8_t i = 0; i < binary_spacer_bit_count; i++){
                    uint32_t bit_mask = (1u << i);
                    uint32_t seperate_conditions = (binary_spacer & bit_mask) >> i;
                    //cout << seperate_conditions << " ";

                    if (seperate_conditions == 0){
                        current_st += st[i + 1];
                    }
                    else if (seperate_conditions == 1){
                        if (set_contains(dictionary, current_st)){
                            seperated_words.push_back(current_st);
                            current_st = st.substr(i + 1, 1);
                        }
                        else{
                            failed = true;
                            break;
                        }

                    }
                    else{
                        throw string("Seperate condition is not binary.");
                    }

                }
                if (!failed && set_contains(dictionary, current_st)){
                    seperated_words.push_back(current_st);
                    possible_sentences.push_back(seperated_words);
                }
            }

            //cout << "===" << endl;
        }
        vector<string> result_sentences_combined;

        for (vector<string> const& v : possible_sentences){
            string combined_sentence;
            for (string const& st2 : v){
                combined_sentence += st2 + " ";
            }
            combined_sentence.pop_back();
            result_sentences_combined.push_back(combined_sentence);
        }

        if (result_sentences_combined.empty()){
            test_file << "      - expect: \"There are no anagrams.\"\n";
        }
        else{
            sort(result_sentences_combined.begin(), result_sentences_combined.end());
            for(string const& result_sentence : result_sentences_combined){
                test_file << "      - expect: \"" + result_sentence + "\"\n";;
            }
        }

        test_file << "      - expect: _EOF_\n";
        cout << "Prepared test case_" + to_string(ind+1) + ": " << original_sentence << endl;
        GlobalPerms.clear();
    }

    test_file << close_string;
    test_file.close();

    return 0;
}
