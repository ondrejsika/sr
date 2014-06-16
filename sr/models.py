from django.db import models

from django.contrib.auth.models import User


class Girl(models.Model):
    name = models.CharField(max_length=128)
    facebook_link = models.URLField(null=True, blank=True)
    picture_link = models.URLField(null=True, blank=True)
    nominated_by = models.ForeignKey(User)

    def __unicode__(self):
        return u'%s' % self.name

    def get_rank_by_user(self, user):
        return GirlRank.get(girl=self, user=user)

    def get_avg_rank(self):
        ranks = []
        for user in User.objects.all():
            rank = self.get_rank_by_user(user=user)
            if rank:
                ranks.append(rank.rank)
        try:
            return sum(ranks) / float(len(ranks))
        except ZeroDivisionError:
            return None


class GirlRank(models.Model):
    girl = models.ForeignKey(Girl)
    user = models.ForeignKey(User)
    rank = models.IntegerField(choices=zip(range(1, 11), range(1, 11)))
    timestamp = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u'%s: %s %s' % (self.user, self.girl, self.rank)

    class Meta:
        ordering = ('-timestamp', )

    @staticmethod
    def get(girl, user):
        try:
            return GirlRank.objects.filter(user=user, girl=girl)[0]
        except IndexError:
            return None
