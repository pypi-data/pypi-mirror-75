import os
import atexit

# os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
import tensorflow_hub as hub
from tensorflow import compat
import matplotlib.pyplot as plt
import numpy as np
from strsimpy.levenshtein import Levenshtein

tf = compat.v1
tf.disable_v2_behavior()

tf_hub_cache_dir = "universal_encoder_cached/"
os.environ["TFHUB_CACHE_DIR"] = tf_hub_cache_dir

# pointing to the folder inside cache dir, it will be unique on your system
module_url = tf_hub_cache_dir + "/d3941dd08d84aba44358d623640d2604d47ffb74/"
# module_url = (
#     "https://tfhub.dev/google/universal-sentence-encoder/1?tf-hub-format=compressed"
# )

# Import the Universal Sentence Encoder's TF Hub module
embed = hub.Module(module_url)
similarity_input_placeholder = tf.placeholder(tf.string, shape=(None))
similarity_message_encodings = embed(similarity_input_placeholder)
session = tf.Session()
session.run(tf.global_variables_initializer())
session.run(tf.tables_initializer())


def getSimilarityScore(sentences):
    message_embeddings_ = session.run(
        similarity_message_encodings,
        feed_dict={similarity_input_placeholder: sentences},
    )

    corr = np.inner(message_embeddings_, message_embeddings_)
    print(corr, sentences)
    # file0.write("{} +++ {}".format(corr, sentences))
    return corr
    # heatmap(sentences, sentences, corr)


def getSimilarity(nlp, maxDialogueTokens, minDialogueTokens, start, end):
    maxWordSnippet = (
        " ".join(maxDialogueTokens[start : end + 1])
        if end
        else " ".join(maxDialogueTokens[start:])
    )
    minWordSnippet = " ".join(minDialogueTokens)

    if maxWordSnippet == "" or minWordSnippet == "":
        return 0.0

    similarity = getSimilarityScore([maxWordSnippet, minWordSnippet])
    return similarity[0][1]


atexit.register(session.close)
