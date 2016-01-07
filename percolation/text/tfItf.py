__doc__="Term frequency - inverse document frequency distance between documents"
from sklearn.feature_extraction.text import TfidfVectorizer

def systemAnalyseAll(sectors_analysis):
    all_texts_measures={}
    for sector in sectors_analysis:
        for data_grouping in sectors_analysis[sector]["tfIdf"]: # texts, authors
            for data_group in sectors_analysis[sector]["tfIdf"][data_grouping]: 
                for measure_group in data_group: # tfIdf, text, texts
                    for measure_type in data_group[measure_group]:
                        for measure_name in data_group[measure_group][measure_type]:
                            measure=data_group[measure_group][measure_type][measure_name]
                            if measure_type=="distances_overall": # distances found in each sector for each text
                                measure_type_="distances_overall"
                                data_grouping_="sectors_text"
                            elif measure_type=="distances_overall_low": # distances found through each author's own texts
                                measure_type_="distances_overall_low"
                                data_grouping_="authors_texts"
                            elif measure_type=="each_text": # each text on the system
                                measure=[measure]
                                measure_type_="each_text_overall"
                                data_grouping_="texts"

                            if measure_type=="distances_overall_authors": # distances found in each sector for each author
                                measure_type_="distances_overall_authors"
                                data_grouping_="authors_texts"
                            elif measure_type=="each_text_author": # text from each author
                                measure_type_="each_text_author"
                                data_grouping_="authors_text"

                            elif measure_type=="numeric_overall": # mean and std of distances from each author
                                measure_type_="numeric_overall"
                                data_grouping_="authors_texts"
                            elif measure_type=="second_numeric": # mean and std of distances from each sector from each author
                                measure_type_="second_numeric_overall"
                                data_grouping_="sectors_authors_text"

                            elif measure_type=="joint_text": # text from each sector
                                measure=[measure]
                                measure_type_="each_text_sector"
                                data_grouping_="sectors_text"
                            elif measure_type=="numeric": # measures of each sector
                                measure=[measure]
                                measure_type_="numeric_overall_high"
                                data_grouping_="sectors"
                            else:
                                raise KeyError("data structure not understood")
                            all_texts_measures[data_grouping_][0][measure_group][measure_type_][measure_name]+=measure
    for data_grouping in all_texts_measures: # texts, authors, authors_text, sectors, sectors_authors
        for data_group in all_texts_measures["data_grouping"]:
          for measure_group in data_group: # tfIdf, text, texts
            for measure_type in data_group[measure_group]: # only list/tuple of strings at first
                for measure_name in all_texts_measures[measure_group][measure_type]:
                    measure=all_texts_measures[measure_group][measure_type][measure_name]
                    if measure_type not in ("each_text_overall","each_text_author","each_text_sector"):
                        mean_val=n.mean(measure)
                        std_val=n.std(  measure)
                        mean_name="M{}".format(measure_name)
                        std_name="D{}".format(measure_name)
                    if measure_type=="each_text_overall": # directly from strings, data_grouping == "strings"
                        tfIdf_matrix=tfIdf(measure)
                        distances=n.hstack(tfIdf_matrix[i][:i] for i in n.arange(tfIdf_matrix.shape[0]))
                        all_texts_measures[data_grouping][0]["tfIdf"]["tfIdf_matrix"]["the_matrix"]=tfIdf_matrix
                        all_texts_measures[data_grouping][0]["tfIdf"]["numeric"]["mdistance"]=n.mean(distances)
                        all_texts_measures[data_grouping][0]["tfIdf"]["numeric"]["ddistance"]=n.std(distances)
                        all_texts_measures[data_grouping][0]["tfIdf"]["distances_overall"]["the_distances"]=distances
                        all_texts_measures[data_grouping][0]["text"]["joint_text"]["the_text"]=" ".join(texts)
                        data_grouping_=data_grouping+"_texts"
                        for text in measure:
                            all_texts_measures[data_grouping_].append({})
                            all_texts_measures[data_grouping_][-1]["texts"]["each_text"]["the_text"]=text
                    if measure_type=="each_text_author": # directly from strings, data_grouping == "strings"
                        tfIdf_matrix=tfIdf(measure)
                        distances=n.hstack(tfIdf_matrix[i][:i] for i in n.arange(tfIdf_matrix.shape[0]))
                        all_texts_measures[data_grouping][0]["tfIdf"]["tfIdf_matrix"]["the_matrix_authors"]=tfIdf_matrix
                        all_texts_measures[data_grouping][0]["tfIdf"]["numeric"]["mdistance_authors"]=n.mean(distances)
                        all_texts_measures[data_grouping][0]["tfIdf"]["numeric"]["ddistance_authors"]=n.std(distances)
                        all_texts_measures[data_grouping][0]["tfIdf"]["distances_overall_authors"]["the_distances"]=distances
                        data_grouping_=data_grouping+"_texts"
                        all_texts_measures[data_grouping_]=[]
                        for text in measure:
                            all_texts_measures[data_grouping_].append({})
                            all_texts_measures[data_grouping_][-1]["texts"]["each_text_authors"]["the_text"]=text
                    if measure_type=="each_text_sector": # directly from strings, data_grouping == "strings"
                        tfIdf_matrix=tfIdf(measure)
                        distances=n.hstack(tfIdf_matrix[i][:i] for i in n.arange(tfIdf_matrix.shape[0]))
                        all_texts_measures[data_grouping][0]["tfIdf"]["tfIdf_matrix"]["the_matrix"]=tfIdf_matrix
                        all_texts_measures[data_grouping][0]["tfIdf"]["numeric"]["mdistance"]=n.mean(distances)
                        all_texts_measures[data_grouping][0]["tfIdf"]["numeric"]["ddistance"]=n.std(distances)
                        all_texts_measures[data_grouping][0]["tfIdf"]["distances_overall"]["the_distances"]=distances
                        data_grouping_=data_grouping+"_texts"
                        all_texts_measures[data_grouping_]=[]
                        for text in measure:
                            all_texts_measures[data_grouping_].append({})
                            all_texts_measures[data_grouping_][-1]["texts"]["each_text_author"]["the_text"]=text
                    elif measure_type=="distances_overall": # data_grouping sectors_texts
                        all_texts_measures[data_grouping][0][measure_group]["numeric"][mean_name]=mean_val
                        all_texts_measures[data_grouping][0][measure_group]["numeric"][std_name]= std_val
                    elif measure_type=="distances_overall_low": # data_grouping texts
                        all_texts_measures[data_grouping][0][measure_group]["numeric"][mean_name]=mean_val
                        all_texts_measures[data_grouping][0][measure_group]["numeric"][std_name]= std_val
                    elif measure_type=="distances_overall_authors": # data_grouping texts
                        all_texts_measures[data_grouping][0][measure_group]["numeric"][mean_name]=mean_val
                        all_texts_measures[data_grouping][0][measure_group]["numeric"][std_name]= std_val
                    elif measure_type=="numeric_overall": # data_grouping texts
                        all_texts_measures[data_grouping][0][measure_group]["second_numeric"][mean_name]=mean_val
                        all_texts_measures[data_grouping][0][measure_group]["second_numeric"][std_name]= std_val
                    elif measure_type=="second_numeric_overall": # data_grouping texts
                        all_texts_measures[data_grouping][0][measure_group]["third_numeric"][mean_name]=mean_val
                        all_texts_measures[data_grouping][0][measure_group]["third_numeric"][std_name]= std_val
                    elif measure_type=="numeric_overall_high": # data_grouping texts
                        all_texts_measures[data_grouping][0][measure_group]["second_numeric_high"][mean_name]=mean_val
                        all_texts_measures[data_grouping][0][measure_group]["second_numeric_high"][std_name]= std_val
                    else:
                        raise KeyError("data structure not understood")
    return all_texts_measures

def sectorsAnalyseAll(authors_analysis,sectorialized_agents):
    all_texts_measures={}
    for agent in sectorialized_agents:
        analysis=authors_analysis[agent]["tfIdf"]
        for data_grouping in analysis: # texts_overall, each_text
            for data_group in analysis[data_grouping]:
                for measure_group in data_group: # tfIdf, text, texts
                    for measure_type in data_group[measure_group]: # tfIdf_matrix, numeric, distances_overall, joint_text, each_text
                        for measure_name in data_group[measure_group][measure_type]: # the_matrix, mdistance, ddistance, the_distances, the_text
                            measure=data_group[measure_group][measure_type][measure_name]
                            if measure_type=="distances_overall": # distances found in each author of the sector
                                measure_type_="distances_overall_low"
                                data_grouping_="texts"
                            elif measure_type=="each_text": # each text in the sector
                                measure=[measure]
                                measure_type_="all_texts"
                                data_grouping_="texts"

                            elif measure_type=="numeric":
                                measure=[measure]
                                measure_type_="numeric_overall"
                                data_grouping_="authors"
                            elif measure_type=="joint_text": # the joint text of each author in the sector
                                measure=[measure]
                                measure_type_="join_text_authors"
                                data_grouping_="authors"
                            else:
                                raise KeyError("data structure not understood")
                            all_texts_measures[data_grouping_][0][measure_group][measure_type_][measure_name]+=measure
    for data_grouping in all_texts_measures: # texts, authors
        for data_group in all_texts_measures[data_grouping]: 
          for measure_group in data_group: # tfIdf, text, texts
            for measure_type in data_group[measure_group]: # only list/tuple of numbers at first
                for measure_name in all_texts_measures[measure_group][measure_type]: # `pos tag`, the_tagged_tokens
                    measure=all_texts_measures[measure_group][measure_type][measure_name]
                    if measure_type not in ("each_text","joint_text_authors"):
                        mean_val=n.mean(measure)
                        std_val=n.std(  measure)
                        mean_name="M{}".format(measure_name)
                        std_name="D{}".format(measure_name)
                    if measure_type=="each_text": # directly from strings, data_grouping == "strings"
                        tfIdf_matrix=tfIdf(measure)
                        distances=n.hstack(tfIdf_matrix[i][:i] for i in n.arange(tfIdf_matrix.shape[0]))
                        all_texts_measures[data_grouping][0]["tfIdf"]["tfIdf_matrix"]["the_matrix"]=tfIdf_matrix
                        all_texts_measures[data_grouping][0]["tfIdf"]["numeric"]["mdistance"]=n.mean(distances)
                        all_texts_measures[data_grouping][0]["tfIdf"]["numeric"]["ddistance"]=n.std(distances)
                        all_texts_measures[data_grouping][0]["tfIdf"]["distances_overall"]["the_distances"]=distances
                        all_texts_measures[data_grouping][0]["text"]["joint_text"]["the_text"]=" ".join(texts)
                        data_grouping_=data_grouping+"_texts"
                        all_texts_measures[data_grouping_]=[]
                        for text in measure:
                            all_texts_measures[data_grouping_].append({})
                            all_texts_measures[data_grouping_][-1]["texts"]["each_text"]["the_text"]=text
                    if measure_type=="joint_text_authors": # directly from strings, data_grouping == "strings"
                        tfIdf_matrix=tfIdf(measure)
                        distances=n.hstack(tfIdf_matrix[i][:i] for i in n.arange(tfIdf_matrix.shape[0]))
                        all_texts_measures[data_grouping][0]["tfIdf"]["tfIdf_matrix_authors"]["the_matrix"]=tfIdf_matrix
                        all_texts_measures[data_grouping][0]["tfIdf"]["numeric"]["mdistance_authors"]=n.mean(distances)
                        all_texts_measures[data_grouping][0]["tfIdf"]["numeric"]["ddistance_authors"]=n.std(distances)
                        all_texts_measures[data_grouping][0]["tfIdf"]["distances_overall_authors"]["the_distances"]=distances
                        data_grouping_=data_grouping+"_texts"
                        all_texts_measures[data_grouping_]=[]
                        for text in measure:
                            all_texts_measures[data_grouping_].append({})
                            all_texts_measures[data_grouping_][-1]["texts"]["each_text_authors"]["the_text"]=text
                    elif measure_type=="distances_overall_low": # data_grouping strings
                        all_texts_measures[data_grouping][0][measure_group]["numeric"][mean_name]=mean_val
                        all_texts_measures[data_grouping][0][measure_group]["numeric"][std_name]= std_val
                    elif measure_type=="numeric_overall": # data_grouping authors
                        all_texts_measures[data_grouping][0][measure_group]["second_numeric"][mean_name]=mean_val
                        all_texts_measures[data_grouping][0][measure_group]["second_numeric"][std_name]= std_val
    return all_texts_measures

def analyseAll(texts):
    texts_measures={"texts_overall":[{"tfIdf":{"tfIds_matrix":{}}}]}
    tfIdf_matrix=tfIdf(texts)
    distances=n.hstack(tfIdf_matrix[i][:i] for i in n.arange(tfIdf_matrix.shape[0]))
    texts_measures["texts_overall"][-1]["tfIdf"]["tfIdf_matrix"]["the_matrix"]=tfIdf_matrix
    texts_measures["texts_overall"][-1]["tfIdf"]["numeric"]["mdistance"]=n.mean(distances)
    texts_measures["texts_overall"][-1]["tfIdf"]["numeric"]["ddistance"]=n.std(distances)
    texts_measures["texts_overall"][-1]["tfIdf"]["distances_overall"]["the_distances"]=distances
    texts_measures["texts_overall"][-1]["text"]["joint_text"]["the_text"]=" ".join(texts)
    texts_measures["each_text"]=[]
    for text in texts:
        texts_measures["each_text"].append({})
        texts_measures["each_text"][-1]["texts"]["each_text"]["the_text"]=texts
    return texts_measures

def tfIdf(texts):
    """Returns distance matrix for the texts"""
    vect = TfidfVectorizer(min_df=1)
    tfidf = vect.fit_transform([tt.lower() for tt in texts])
    aa=(tfidf * tfidf.T).A
    return aa
