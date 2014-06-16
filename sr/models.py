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
            return sum(ranks) / len(ranks)
        except ZeroDivisionError:
            return None

    def get_rank_count(self):
        count = 0
        for user in User.objects.all():
            rank = self.get_rank_by_user(user=user)
            if rank:
                count += 1
        return count

    def get_max_rate(self):
        ranks = []
        min_ranks = []
        for user in User.objects.all():
            rank = self.get_rank_by_user(user)
            if rank:
                ranks.append(rank)
        if len(ranks) == 0:
            return None
        ranks = sorted(ranks, key=lambda obj: obj.rank)
        ranks = list(reversed(ranks))
        min_rank = ranks[0].rank
        for rank in ranks:
            if rank.rank == min_rank:
                min_ranks.append(rank)
            else:
                return min_ranks

    def get_min_rate(self):
        ranks = []
        min_ranks = []
        for user in User.objects.all():
            rank = self.get_rank_by_user(user)
            if rank:
                ranks.append(rank)
        if len(ranks) == 0:
            return None
        ranks = sorted(ranks, key=lambda obj: obj.rank)
        min_rank = ranks[0].rank
        for rank in ranks:
            if rank.rank == min_rank:
                min_ranks.append(rank)
            else:
                return min_ranks

    def get_history_max_rate(self):
        min_ranks = []
        ranks = GirlRank.objects.filter(girl=self).order_by('-rank')
        if len(ranks) == 0:
            return None
        min_rank = ranks[0].rank
        for rank in ranks:
            if rank.rank == min_rank:
                min_ranks.append(rank)
            else:
                return min_ranks

    def get_history_min_rate(self):
        min_ranks = []
        ranks = GirlRank.objects.filter(girl=self).order_by('rank')
        if len(ranks) == 0:
            return None
        min_rank = ranks[0].rank
        for rank in ranks:
            if rank.rank == min_rank:
                min_ranks.append(rank)
            else:
                return min_ranks



class GirlRank(models.Model):
    RANKS = zip(map(lambda n: n/2.0, range(0, 21)), map(lambda n: n/2.0, range(0, 21)))
    girl = models.ForeignKey(Girl)
    user = models.ForeignKey(User)
    rank = models.DecimalField(decimal_places=1, max_digits=3, choices=RANKS)
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


class GirlComment(models.Model):
    girl = models.ForeignKey(Girl)
    user = models.ForeignKey(User)
    deleted = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    text = models.TextField()

    def __unicode__(self):
        return u'%s: %s, %s' % (self.user, self.girl, self.text[:20])

