import requests


class NvwaPredict(object):

    def __init__(self, host, port, endpoint):
        self.host = host
        self.port = port
        self.endpoint = endpoint

        self.dim_name = {
            "1": "AchievementOriented",
            "2": "Innovation",
            "3": "LearningAbility",
            "4": "Resilience",
            "5": "Execution",
            "6": "TeamWork",
        }

    def predict(self, doc_text, model_type: int):
        purl = f"{self.host}:{self.port}/{self.endpoint}"
        pdata = {
            "params": {
                "docText": doc_text,
                "model_type": model_type
            }
        }
        header = {
            "Content-Type": "application/json",
            "Auth": "dc5976de",
        }
        resp = requests.post(purl, json=pdata, headers=header)
        return resp.json()["result"]

    def predict_all(self, doc_text):
        pre_result = {}

        for i in range(1, 7):
            pre_score = self.predict(doc_text, i)
            pre_result[str(i)] = pre_score * 0.01
        return pre_result


class SimPredict(object):

    def __init__(self, host, port, endpoint, auth):
        self.host = host
        self.port = port
        self.endpoint = endpoint
        self.auth = auth

    def predict(self, doc, sta):
        purl = f"{self.host}:{self.port}/{self.endpoint}"
        pdata = {
            "params": {
                "docText": doc,
                "template": sta
            }
        }
        header = {
            "Content-Type": "application/json",
            "Auth": self.auth,
        }
        resp = requests.post(purl, json=pdata, headers=header)
        return resp.json()["result"]

    def predict_all(self, docs, stas):
        pre_result = []

        for i, doc in enumerate(docs):
            sta = stas[i]
            pre_score = self.predict(doc, sta)
            pre_result.append(pre_score * 0.01)
        return pre_result


if __name__ == '__main__':
    """
    1: AchievementOriented
    2: Innovation
    3: LearningAbility
    4: Resilience
    5: Execution
    6: TeamWork
    """

    # doc_text = "fgdgdg"
    # doc_text = "呃，这个好像嗯是一次。嗯，机械设计的课程设计，当时我们是要设计一个呃减速器。二级减速器，然后当时是呢，根据机械原理，做过的一次呃。呃，课程设计，然后把上把几元的课程设计的。嗯，方案用用，现在的一个方案去。呃，拍给具体的时间出来。然后机械原理的课程设计是嗯。嗯。呃，当时对机械设计不太了解，然后那个方案是做的有问题的。然后就在呃，机械设计呃。嗯。机械设计师的课程设计的时候，我们需要把它。呃方案给具体做出来的时候，嗯。呃，做出做最后做出来的呃。那个尺寸是呃有问题的不对的，然后我们就。对我我们就要去对那个方案进行重新重新的呃，纠正。然后。然后当时时间，嗯也有点紧可能呃去重新做也来不及了。然后就只能在原有的。呃，原有的词上面去呃修改，在原有图纸上面去修改。然后我喝。我就嗯。呃去。嗯。主导那个呃。方案的重新的一个修改和尺寸的重新的一个标定。最后还是用。哦哦。最后设计出来的还是。呃，符合一个课程设计的要求的。"
    doc_text = "呃，这个好像嗯是一次。"
    doc_text1 = "[MASK]"
    # nmodel = NvwaPredict("http://model.ai-open.hrtps.com", 80, "/models/NvWaChineseLeo/transfer")
    nmodel = SimPredict("http://model.ai-open.hrtps.com", 80, "/models/PanGuChineseLeo/transfer", auth="dc5976de")
    # pre = nmodel.predict(doc_text1, 1)
    # pre = nmodel.predict_all(doc_text1)
    # print(pre)
    pre = nmodel.predict(doc_text, doc_text1)

    print(pre)
