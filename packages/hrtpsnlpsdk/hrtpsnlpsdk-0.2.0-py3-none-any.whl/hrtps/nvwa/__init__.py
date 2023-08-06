import requests
from tqdm import tqdm


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
        purl = f"http://{self.host}:{self.port}/{self.endpoint}"
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
        purl = f"http://{self.host}:{self.port}/{self.endpoint}"
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
    # doc_text = "在上半年PR Lab实习期间，同项目组的同事来自不同的国家，相较之下，美国人拥有语言优势与更多的人脉资源，中国人在策划与物料制作方面能力突出。在团度合作初始阶段，任务分派都是遵循个人意愿，结果擅长做前台联络的人却领了幕后工作的活，工作进度慢且成果不佳。在此情况下，我建议团队坐在一起进行深入的沟通，坦诚分析各自的优劣势，明确自己最合适的工作岗位。在沟通确认后，团队成员达成一致，由美国人领头客户沟通与联络媒体记者等工作，由中国人主要担任方案撰写与物料制作的任务。大家各司其职，发挥各自优势，成功为客户举办了多次活动。"
    doc_text = "嗯。嗯。呃，我想举一个在国药物流的例子，当时我在客户服务部担任客户服务代表，然后当时领导委派的任务是在一个月内上线他们的自动机废话自动电算化计费项目，当时这个任务是非常重要的，且非常紧迫的，因此，首先我给自己每天的工作时间做了规划，每天下午一点到四点，然后早上十点到11点都会给全新留给这个任务，在其他的时间处理，剩下的杂物然后其次，嗯确认一下，我和。我为了完成这个任务需要沟通，不沟通的部门，当时是主要要沟通的是it部门和仓储部门啊，挨和仓储部门也是要确认的是客户的计费口径，然后如果出现问题。我会先进行核对和it部门进行的沟通主要是每个计费项目怎么落实。所以，因为当时it部门人手比较紧张，我为了节省效率，提高效率，我每次都会尝试去定位可能存在的问题，然后提前写好这样一条条罗列给他们，然后和仓储部门的话，我也会提前准备好对账是电脑进行计算和我自己进行计算哪里出现了问题都可能存在的问题都分析给他们，然后一一罗列给他们每最后在每周的时候每天结束的时候，呃，发微信发QQ给他了。对，然后第二天早上的时候我也会及时的人到他们办公室进行跟进，一定要人到办公室，因为这样的话。可以更好的完成任务，因为当时可能对于it。对于仓储部门来说，我这边的需求不是最紧急的，因此，为了我，我为了完成我的任务会人进行过去进行盯一下，然后每天确保前一天问他的问题，第二天呢，给我进行反馈，这样的话，按照我既定的流程，每天定好的时间会一步步稳步推进，比如说我可能一共一个月的时间前两周我要做十几五家客户后两周要做八家客户，这样子的话，按照时间节点，如果超过时间节点会加快进度稍微的加一下班对主要是这个样子。"
    # doc_text = "嗯呃，面试官，你好，我所举的案例是发生于二零，嗯，在我。大学期间所发生的一个紧急任务，这个任务就是。那个当时突然就是在我大学的时候突然发生了那个西门子杯中国智能挑战赛，然后举办任务交给了我们学校我们实验室，然后当时我作为我们实验室的负责人呃，就需要把这个任务进行完成，然后当我接受了这个任务的时候，首先我用最快的时间来梳理了一下举办这个比啊。举办这个比赛我手头的工作就是需要做哪些事儿。然后，比如说做宣讲。然后找校领导盖章。审批场地，然后参会人员邀请等事儿，然后我对这些事儿进行了那个一个听众一个轻重缓急的分分配以及哪些任务自己可以独立完成哪些任务需要别人协助，同时我分析了我们实验室。呃，可以帮助我完成这个比赛承办的一些人员的性格特点。然后根据他们的性格特点以及能力特点，呃，将其中的一些任务对对他们进行了分配，比如说我们实验室成员有一个是外联部长。然后我们就我们就让他去拉了新东方的赞助。啊，还有我们有一个人是在他在我们实验室工作的同时是学办成员，然后我就将。呃。参参赛的那个材料审批交给了她，由她去找。学办主任以及校长去盖章，同时，呃，为了比赛能够顺利举行。呃，我去，呃，我准备制定一个我们学院那个宣讲会嘛，在我们学校举办宣讲会，呃，对于这个宣讲会。首先我对这个宣讲会的场地。以及参会人员参会领导。近啊，明香对名单进行确认啊，并对一些领导的时间进行确定。然后进行那个。那个宣讲会的宣讲啊，最最后还有那个。相关参赛学校的邀请，这个也是通过我们和。啊，赛事的主。方及西门子，西门子公司进行交涉来确定。大概参加的会有哪些学校，然后与他们学校相关新闻直播的负责人我来继续进行联系。嗯，同时来确定他们是否来参加比赛以及初赛筛选是如何进行。嗯，在这个比赛中其实还遇到一个问题就是。嗯。在那个。场地审批场地审批上，然后因为当时不是这个比赛是在暑假举行吗，所以会有相关领导。都都已经。都已经放假了，然后那个场地不好申请，但同时作为一个省级赛事。它的举办场地有一定规模的要求，然后这时候我知道这个事儿是我自己。去沟通协调，无法完成的，然后，首先我就找到了我们实验室的负责老师，并通过他。去联系我们院长在通过我们院长。去联系了，我们学校主管活动赛事举办的副校长然后最终将呃将那个实验场地。皮板下来啊，对于这个比赛。然后接下来场地有了然后宣讲确定参赛名单，一切事儿都完成之后。只剩比赛举办，同时我们考虑了比赛中可能发生的突发问题，比如设备故障。系咯。啊，我们邀请了一些。有一个西门子的赛事负责人，包括我们。那个西门子大赛中国智能挑战赛前几年获奖的获得特等奖的技术人员来我们提供技术保障。另外一个突发事件，比如图呃，因为在夏天嘛，突然有人中暑或者生病。这个问题我们也联系了我们的校医院。啊，设置了救护车进行那个。进行问题的解决就是相关预警的解决。同时，我们通过拉赞助获得了新东方和娃哈哈的赞助。在确保了日常供应的水。等相关需求的解决，嗯。然后，其次我们又当时有我还有另外两个实验室的夫。负负责人，我们三个组成了一个应急保障团队来确保当有应急情况发生时有人可以解决问题。啊，大概就是这些，谢谢面试官。"
    # doc_text = "121"
    # doc_text1 = "[MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK][MASK]"
    # nmodel = NvwaPredict("model.ai-open.hrtps.com", 80, "/models/NvWaChineseLeo/transfer")
    # nmodel = NvwaPredict("model.ai-open.hrtps.com", 80, "/models/NvWaChineseLeo/transfer")
    nmodel = SimPredict("model.ai-open.hrtps.com", 80, "/models/PanGuChineseLeo/transfer", auth="dc5976de")
    for i in tqdm(range(1, 7)):
        # pre = nmodel.predict(doc_text, i)
    # pre = nmodel.predict_all(doc_text1)
    # print(pre)
        pre = nmodel.predict(doc_text, doc_text)

        print(f"{i}\t{pre}")
        # print(pre)
