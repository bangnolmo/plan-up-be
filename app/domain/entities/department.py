class Department:

    #학과 초기화
    def __init__(self, hakgwa_cd, hakgwa_name, parent_cd=None):
        self.hakgwa_cd = hakgwa_cd
        self.hakgwa_name = hakgwa_name
        self.parent_cd = parent_cd

    #__dict__로 반환
    def to_dict(self):
        return vars(self)