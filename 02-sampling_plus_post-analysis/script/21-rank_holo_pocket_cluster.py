
def read_cluster_ids(filepath):
    cluster_ids = {}
    with open(filepath, 'r') as file:
        next(file)  # Skip the first line
        for line in file:
            parts = line.split()
            if len(parts) >= 2:
                model_id = parts[0]
                cluster_id = parts[1]
                cluster_ids[model_id] = cluster_id
    return cluster_ids

def process_summary(filepath, cluster_ids):
    cluster_lines = {}
    with open(filepath, 'r') as file:
        for lineno, line in enumerate(file, 1):
            parts = line.strip().split(',')
            if len(parts) > 2:
                model_id = str(lineno)  # Use line number as model id
                try:
                    rtmscore = float(parts[2])
                except ValueError:
                    # Set rtmscore to 0.0 if conversion fails
                    rtmscore = 0.0

                if model_id in cluster_ids:
                    cluster_id = cluster_ids[model_id]
                    if cluster_id not in cluster_lines:
                        cluster_lines[cluster_id] = []
                    cluster_lines[cluster_id].append((line, rtmscore))
    return cluster_lines

def write_clusters_and_top_scores(cluster_lines, cluster_file, top_scores_file):
    with open(cluster_file, 'w') as cluster_out, open(top_scores_file, 'w') as scores_out:
        for cluster_id, lines in cluster_lines.items():
            top_line = max(lines, key=lambda x: x[1])[0]
            scores_out.write(top_line)
            for line, _ in lines:
                cluster_out.write(f"Cluster {cluster_id}: {line}")

cluster_ids = read_cluster_ids('./20-cluster/cnumvstime.dat')
cluster_lines = process_summary('19-summary.txt', cluster_ids)
write_clusters_and_top_scores(cluster_lines, '21_holo_pocket_cluster.txt', '21_holo_pocket_rank1.txt')

with open("21_holo_pocket_rank1.txt", "r") as f:
    lines = f.readlines()

sorted_lines = sorted(lines, key=lambda x: float(x.strip().split(",")[2]), reverse=True)

with open("21_holo_pocket_rank_sort.txt", "w") as f:
    f.writelines(sorted_lines)