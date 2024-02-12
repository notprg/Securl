cd load_data
docker build --tag load_data .
docker tag load_data prg10/load_data
docker push docker.io/prg10/load_data
cd ..
cd sgd
docker build --tag sgd .
docker tag sgd prg10/sgd
docker push docker.io/prg10/sgd
cd ..
cd random_forest
docker build --tag random_forest .
docker tag random_forest prg10/random_forest
docker push docker.io/prg10/random_forest
cd ..
cd naive_bayes
docker build --tag naive_bayes .
docker tag naive_bayes prg10/naive_bayes
docker push docker.io/prg10/naive_bayes
cd ..
cd app
docker build --tag malicious_url_detection_v2 .
docker tag malicious_url_detection_v2 prg10/malicious_url_detection_v2
docker push docker.io/prg10/malicious_url_detection_v2
cd ..
