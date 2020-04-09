##{
# System configuration
required_data_path = '/home/mgarort/repos/TOPOS/topos/required_data/'

# User options
prediction_mode = 'retrained'     # one of 'pretrained' or 'retrained'
normalization = 'self'  # one of 'self' (adjust with own mean and std) or 'train' (adjust with training set's mean and std)
n_genes = 110 # if prediction-mode is pretrained, n_genes will always be 110
input_matrix = '/home/mgarort/repos/TOPOS/topos/playground/sample_input_matrices/X_primary_1.tsv'
##}


##{
# Load required modules
import pandas as pd
from sklearn.preprocessing import StandardScaler,LabelEncoder
from sklearn.svm import SVC
##}

	
##{
df_user = pd.read_table(input_matrix, index_col=0)
df_user.columns = [str(elem) for elem in df_user.columns]
df_ranking = pd.read_table(required_data_path + 'rfe_ranking.tsv')
df_ranking['entrez_id'] = df_ranking['entrez_id'].astype(str)
##}


##{
# Keep only the genes that are going to be used in the prediction (either the 110 selected genes if pretrained, or n_best_genes if we're gonna retrain)
if prediction_mode == 'pretrained':
	n_genes = 110
	best_n_genes = df_ranking.loc[df_ranking['ranking'] <= int(n_genes),'entrez_id']
	if (~best_n_genes.isin(df_user.columns)).any():
		raise ValueError('The following genes are not provided. Expression values for these genes are required when choosing the prediction mode "pretrained". If you do not have this information, use the prediction mode "retrained" instead. You will also need to download the training matrix. Entrez ids: {}'.format(best_n_genes.loc[~best_n_genes.isin(df_user.columns)].values))
else:
	best_n_genes = df_ranking.loc[df_ranking['ranking'] <= int(n_genes),'entrez_id']
	best_n_genes = best_n_genes.loc[best_n_genes.isin(df_user.columns)]
        
X_user = df_user.loc[:,best_n_genes]
##}


##{
# Normalize
if normalization == 'self':
	scaler = StandardScaler().fit(X_user)
	X_user_scl = pd.DataFrame(scaler.transform(X_user), index=X_user.index, columns=X_user.columns)
else:
	genes_mean_std = pd.read_table(required_data_path + 'genes_mean_and_std.tsv',index_col=0)
	genes_mean_std.index = [str(elem) for elem in genes_mean_std.index]
	X_user_scl = (X_user - genes_mean_std.loc[X_user.columns,'mean'])/(genes_mean_std.loc[X_user.columns,'std'])
##}


##{
# Load pretrained classifier or train a new one
if prediction_mode == 'pretrained':
	from sklearn.externals import joblib
	clf = joblib.load(required_data_path + 'clf_pretrained_110.pkl')
	encoder = joblib.load(required_data_path + 'label_encoder.pkl')
else:
	df_train = pd.read_pickle(required_data_path + 'df_train_prim_met_lines.pkl')
	X_train_scl = df_train.iloc[:,:-1]
	X_train_scl = X_train_scl.loc[:,best_n_genes]
	encoder = LabelEncoder().fit(df_train.iloc[:,-1])
	Y_train = encoder.transform(df_train.iloc[:,-1])
	clf = SVC(kernel='linear',C=1).fit(X_train_scl,Y_train)
##}


##{
# Predict top prediction
P_top_intlabel = clf.predict(X_user_scl)
P_top_wordlabel = pd.Series(encoder.inverse_transform(P_top_intlabel),index=X_user_scl.index)
##}


##{
# Predict top K prediction. K is the desired ranking of the prediction. If K=1, then we would get the usual top prediction. If K=2, then we would get the second best prediction. Etc.
K = 2 
P_topK_intlabel = np.argsort(clf.decision_function(X_user_scl))[:,-K]
P_topK_wordlabel = pd.Series(encoder.inverse_transform(P_topK_intlabel))
##}


##{
# Check that the predictions are right (not sure if this makes sense scientifically bc I don't remember where the sample matrices come from; I'm just making sure that I haven't messed up the code)
Y_top_wordlabel = pd.read_csv('/home/mgarort/repos/TOPOS/topos/playground/sample_input_matrices/Y_primary_1.tsv',sep='\t')
##}
