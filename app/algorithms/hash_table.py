class MyHashMap:
    MAX_LOAD_FACTOR = 0.75

    def __init__(self, capacity=8):
        self.capacity = capacity
        self.size = 0
        self.buckets = [[] for _ in range(capacity)]
        self.all_apps_list = [] 

    def _index(self, key):
        hash_value = 0
        for char in key:
            hash_value = (hash_value * 31 + ord(char)) % self.capacity
        return hash_value

    def load_factor(self):

        return self.size / self.capacity

    def _resize(self):
        old_buckets = self.buckets

        self.capacity *= 2
        self.buckets = [[] for _ in range(self.capacity)]

        for bucket in old_buckets:
            for key, value in bucket:
                index = self._index(key)
                self.buckets[index].append((key,value))

    def put(self, key, value):
        index = self._index(key)
        bucket = self.buckets[index]

        for i, (existing_key, existing_value) in enumerate(bucket):
            if existing_key == key:
                bucket[i] = (key, value)
                
                return

        if (self.size + 1) / self.capacity > self.MAX_LOAD_FACTOR:
                    self._resize()

                    index = self._index(key)
                    bucket = self.buckets[index]

        bucket.append((key, value))
        self.size += 1

        if isinstance(value, dict):
            value["app_id"] = key
            
        self.all_apps_list.append(value)  

        

    def get(self, key):
        index = self._index(key)
        bucket = self.buckets[index]

        for existing_key, value in bucket:
            if existing_key == key:
                
                return value

        return None

    def contains(self, key):
        return self.get(key) is not None

    def remove(self, key):
        index = self._index(key)
        bucket = self.buckets[index]

        for i, (existing_key, value) in enumerate(bucket):
            if existing_key == key:
                bucket.pop(i)
                self.size -= 1
                
                return True

        return False

    def __len__(self):
        return self.size

    def stats(self):

        return{
            "size": self.size,
            "capacity": self.capacity,
            "load_factor": round(self.load_factor(), 4),
        }
        