from django.db import models
import datetime

class People(models.Model):
    id = models.IntegerField(db_column='ID', blank=True, null=False, primary_key=True)  # Field name made lowercase.
    playerid = models.TextField(db_column='playerID', blank=True, null=False, unique=True)  # Field name made lowercase.
    birthyear = models.IntegerField(db_column='birthYear', blank=True, null=True)  # Field name made lowercase.
    birthmonth = models.IntegerField(db_column='birthMonth', blank=True, null=True)  # Field name made lowercase.
    birthday = models.IntegerField(db_column='birthDay', blank=True, null=True)  # Field name made lowercase.
    birthcity = models.TextField(db_column='birthCity', blank=True, null=True)  # Field name made lowercase.
    birthcountry = models.TextField(db_column='birthCountry', blank=True, null=True)  # Field name made lowercase.
    birthstate = models.TextField(db_column='birthState', blank=True, null=True)  # Field name made lowercase.
    deathyear = models.IntegerField(db_column='deathYear', blank=True, null=True)  # Field name made lowercase.
    deathmonth = models.IntegerField(db_column='deathMonth', blank=True, null=True)  # Field name made lowercase.
    deathday = models.IntegerField(db_column='deathDay', blank=True, null=True)  # Field name made lowercase.
    deathcountry = models.TextField(db_column='deathCountry', blank=True, null=True)  # Field name made lowercase.
    deathstate = models.TextField(db_column='deathState', blank=True, null=True)  # Field name made lowercase.
    deathcity = models.TextField(db_column='deathCity', blank=True, null=True)  # Field name made lowercase.
    namefirst = models.TextField(db_column='nameFirst', blank=True, null=True)  # Field name made lowercase.
    namelast = models.TextField(db_column='nameLast', blank=True, null=True)  # Field name made lowercase.
    namegiven = models.TextField(db_column='nameGiven', blank=True, null=True)  # Field name made lowercase.
    weight = models.IntegerField(blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)
    bats = models.TextField(blank=True, null=True)
    throws = models.TextField(blank=True, null=True)
    debut = models.TextField(blank=True, null=True)
    bbrefid = models.TextField(db_column='bbrefID', blank=True, null=True)  # Field name made lowercase.
    finalgame = models.TextField(db_column='finalGame', blank=True, null=True)  # Field name made lowercase.
    retroid = models.TextField(db_column='retroID', blank=True, null=True)  # Field name made lowercase.

    def get_full_name(self):
        return f'{self.namefirst} {self.namelast} {self.namegiven}'

    def get_date_of_birth(self):
        if not self.birthyear: self.birthyear = 1
        if not self.birthmonth: self.birthmonth = 1
        if not self.birthday: self.birthday = 1
        return datetime.datetime(self.birthyear, self.birthmonth, self.birthday)

    def get_data_for_radio(self):
        data = dict()
        data['weight'] = self.weight
        data['height'] = self.height
        gp = list(map(lambda k: int(k), list(self.batting_set.values_list("ab", flat=True))))
        h = list(map(lambda k: int(k), list(self.batting_set.values_list("h", flat=True))))
        hr = list(map(lambda k: int(k), list(self.batting_set.values_list("h", flat=True))))
        #data['ab_sum'] = sum(gp)
        data['h_avg'] = 0 if sum(gp) == 0 else sum(h)/sum(gp)
        data['hr_avg'] = 0 if sum(gp) == 0 else sum(hr)/len(gp)
        games = list(map(lambda k: int(k), list(self.pitching_set.values_list("g", flat=True))))
        era = list(map(lambda k: int(k), list(self.batting_set.values_list("era", flat=True))))
        so = list(map(lambda k: int(k), list(self.batting_set.values_list("so", flat=True))))
        data['era'] = 0 if len(era) == 0 else sum(era)/len(era)
        data['so'] = 0 if len(so) == 0 else sum(so)/len(so)
        print(data)
        return data


    def __str__(self):
        return str(self.id) +" | " + self.get_full_name() + str(self.get_date_of_birth())

    class Meta:
        managed = False
        db_table = 'People'


class Batting(models.Model):
    playerid = models.ForeignKey(People, to_field="playerid", on_delete=models.CASCADE, db_column='playerID', blank=False, null=False)  # Field name made lowercase.
    yearid = models.IntegerField(db_column='yearID', blank=False, null=False, primary_key=True)  # Field name made lowercase.
    stint = models.IntegerField(blank=True, null=True)
    teamid = models.TextField(db_column='teamID', blank=True, null=True)  # Field name made lowercase.
    lgid = models.TextField(db_column='lgID', blank=True, null=True)  # Field name made lowercase.
    g = models.IntegerField(db_column='G', blank=True, null=True)  # Field name made lowercase.
    g_batting = models.IntegerField(db_column='G_batting', blank=True, null=True)  # Field name made lowercase.
    ab = models.IntegerField(db_column='AB', blank=True, null=True)  # Field name made lowercase.
    r = models.IntegerField(db_column='R', blank=True, null=True)  # Field name made lowercase.
    h = models.TextField(db_column='H', blank=True, null=True)  # Field name made lowercase.
    number_2b = models.TextField(db_column='2B', blank=True, null=True)  # Field name made lowercase. Field renamed because it wasn't a valid Python identifier.
    number_3b = models.TextField(db_column='3B', blank=True, null=True)  # Field name made lowercase. Field renamed because it wasn't a valid Python identifier.
    hr = models.TextField(db_column='HR', blank=True, null=True)  # Field name made lowercase.
    rbi = models.TextField(db_column='RBI', blank=True, null=True)  # Field name made lowercase.
    sb = models.TextField(db_column='SB', blank=True, null=True)  # Field name made lowercase.
    cs = models.TextField(db_column='CS', blank=True, null=True)  # Field name made lowercase.
    bb = models.TextField(db_column='BB', blank=True, null=True)  # Field name made lowercase.
    so = models.TextField(db_column='SO', blank=True, null=True)  # Field name made lowercase.
    ibb = models.TextField(db_column='IBB', blank=True, null=True)  # Field name made lowercase.
    hbp = models.TextField(db_column='HBP', blank=True, null=True)  # Field name made lowercase.
    sh = models.TextField(db_column='SH', blank=True, null=True)  # Field name made lowercase.
    sf = models.TextField(db_column='SF', blank=True, null=True)  # Field name made lowercase.
    gidp = models.TextField(db_column='GIDP', blank=True, null=True)  # Field name made lowercase.
    g_old = models.TextField(db_column='G_old', blank=True, null=True)  # Field name made lowercase.

    def __str__(self):
        return str([self.yearid, self.teamid, self.g_batting, self.r, self.h])
    def get_info(self):
        return [self.yearid, self.teamid, self.g_batting, self.r, self.h]

    class Meta:
        managed = False
        db_table = 'Batting'
        unique_together = ('playerid', 'yearid')


class Fielding(models.Model):
    playerid = models.TextField(db_column='playerID', blank=True, null=True)  # Field name made lowercase.
    yearid = models.IntegerField(db_column='yearID', blank=True, null=True)  # Field name made lowercase.
    stint = models.IntegerField(blank=True, null=True)
    teamid = models.TextField(db_column='teamID', blank=True, null=True)  # Field name made lowercase.
    lgid = models.TextField(db_column='lgID', blank=True, null=True)  # Field name made lowercase.
    pos = models.TextField(db_column='POS', blank=True, null=True)  # Field name made lowercase.
    g = models.IntegerField(db_column='G', blank=True, null=True)  # Field name made lowercase.
    gs = models.IntegerField(db_column='GS', blank=True, null=True)  # Field name made lowercase.
    innouts = models.IntegerField(db_column='InnOuts', blank=True, null=True)  # Field name made lowercase.
    po = models.IntegerField(db_column='PO', blank=True, null=True)  # Field name made lowercase.
    a = models.IntegerField(db_column='A', blank=True, null=True)  # Field name made lowercase.
    e = models.TextField(db_column='E', blank=True, null=True)  # Field name made lowercase.
    dp = models.TextField(db_column='DP', blank=True, null=True)  # Field name made lowercase.
    pb = models.TextField(db_column='PB', blank=True, null=True)  # Field name made lowercase.
    wp = models.TextField(db_column='WP', blank=True, null=True)  # Field name made lowercase.
    sb = models.TextField(db_column='SB', blank=True, null=True)  # Field name made lowercase.
    cs = models.TextField(db_column='CS', blank=True, null=True)  # Field name made lowercase.
    zr = models.TextField(db_column='ZR', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Fielding'


class Pitching(models.Model):
    playerid = models.ForeignKey(People, to_field="playerid", on_delete=models.CASCADE, db_column='playerID', blank=True, null=True)  # Field name made lowercase.
    yearid = models.IntegerField(db_column='yearID', blank=False, null=False, primary_key=True)  # Field name made lowercase.
    stint = models.IntegerField(blank=True, null=True)
    teamid = models.TextField(db_column='teamID', blank=True, null=True)  # Field name made lowercase.
    lgid = models.TextField(db_column='lgID', blank=True, null=True)  # Field name made lowercase.
    w = models.IntegerField(db_column='W', blank=True, null=True)  # Field name made lowercase.
    l = models.IntegerField(db_column='L', blank=True, null=True)  # Field name made lowercase.
    g = models.IntegerField(db_column='G', blank=True, null=True)  # Field name made lowercase.
    gs = models.IntegerField(db_column='GS', blank=True, null=True)  # Field name made lowercase.
    cg = models.IntegerField(db_column='CG', blank=True, null=True)  # Field name made lowercase.
    sho = models.IntegerField(db_column='SHO', blank=True, null=True)  # Field name made lowercase.
    sv = models.IntegerField(db_column='SV', blank=True, null=True)  # Field name made lowercase.
    ipouts = models.IntegerField(db_column='IPouts', blank=True, null=True)  # Field name made lowercase.
    h = models.IntegerField(db_column='H', blank=True, null=True)  # Field name made lowercase.
    er = models.IntegerField(db_column='ER', blank=True, null=True)  # Field name made lowercase.
    hr = models.IntegerField(db_column='HR', blank=True, null=True)  # Field name made lowercase.
    bb = models.IntegerField(db_column='BB', blank=True, null=True)  # Field name made lowercase.
    so = models.IntegerField(db_column='SO', blank=True, null=True)  # Field name made lowercase.
    baopp = models.TextField(db_column='BAOpp', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    era = models.TextField(db_column='ERA', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    ibb = models.IntegerField(db_column='IBB', blank=True, null=True)  # Field name made lowercase.
    wp = models.IntegerField(db_column='WP', blank=True, null=True)  # Field name made lowercase.
    hbp = models.IntegerField(db_column='HBP', blank=True, null=True)  # Field name made lowercase.
    bk = models.IntegerField(db_column='BK', blank=True, null=True)  # Field name made lowercase.
    bfp = models.IntegerField(db_column='BFP', blank=True, null=True)  # Field name made lowercase.
    gf = models.IntegerField(db_column='GF', blank=True, null=True)  # Field name made lowercase.
    r = models.TextField(db_column='R', blank=True, null=True)  # Field name made lowercase.
    sh = models.TextField(db_column='SH', blank=True, null=True)  # Field name made lowercase.
    sf = models.TextField(db_column='SF', blank=True, null=True)  # Field name made lowercase.
    gidp = models.TextField(db_column='GIDP', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Pitching'
        unique_together = ('playerid', 'yearid')
