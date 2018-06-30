from ..main import MetalMaxHack


class Tool(MetalMaxHack):
    from . import models, datasets

    @property
    def chariot_equips(self):
        from . import chariot_equips
        return chariot_equips
    

    def render_person_ext(self):
        datasets = self.datasets
        # for i, label in enumerate(datasets.SUBPROFS[1:]):
        #     ModelInput("subprof_levels.%d" % i, "%s等级" % label)
        #     ModelInput("subprof_exps.%d" % i, "%s经验" % label)
        # for i in range(self.person.skill_counts.length):
        #     ModelInput("skill_counts.%d" % i, "技能%d次数" % (i + 1))
        # for i in range(self.person.subskill_counts.length):
        #     ModelInput("subskill_counts.%d" % i, "副职业技能%d次数" % (i + 1))