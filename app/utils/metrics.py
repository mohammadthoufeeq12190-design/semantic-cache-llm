class Metrics:
    def __init__(self):
        self.total_requests = 0
        self.cache_hits = 0
        self.cache_misses = 0
        self.total_latency = 0

    def record_hit(self, latency):
        self.total_requests += 1
        self.cache_hits += 1
        self.total_latency += latency

    def record_miss(self, latency):
        self.total_requests += 1
        self.cache_misses += 1
        self.total_latency += latency

    def summary(self):
        avg_latency = (
            self.total_latency / self.total_requests
            if self.total_requests > 0
            else 0
        )
        hit_rate = (
            self.cache_hits / self.total_requests * 100
            if self.total_requests > 0
            else 0
        )

        return {
            "total_requests": self.total_requests,
            "cache_hits": self.cache_hits,
            "cache_misses": self.cache_misses,
            "hit_rate_percent": round(hit_rate, 2),
            "average_latency_seconds": round(avg_latency, 4),
        }


metrics = Metrics()