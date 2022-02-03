import os
basepath = os.getcwd()

path = basepath

#
# Prepare my job script!
#

# remove all by hand in case of job retry... NOTE: some jobs needs to recover s
exec_cmd = "(rm -rf .complete || true) && " # some protections
exec_cmd = "(rm -rf rxccore || true) && " # some protections
exec_cmd = "(rm -rf rxcnn || true) && " # some protections

# download all necessary local packages...
exec_cmd+= "git clone https://github.com/bric-tb-softwares/rxcore.git && "
exec_cmd+= "git clone https://github.com/bric-tb-softwares/rxcnn.git && "
# setup into the python path
exec_cmd+= "cd rxcore && export PYTHONPATH=$PYTHONPATH:$PWD/rxcore && cd .. && "
exec_cmd+= "cd rxcnn && export PYTHONPATH=$PYTHONPATH:$PWD/rxcnn && cd .. && "

# execute my job!
exec_cmd+= "python rxcnn/versions/job_tuning.py -j %IN -i %DATA -v %OUT && "

# if complete, remove some dirs...
exec_cmd+= "rm -rf rxwgan && rm -rf rxcore"

command = """maestro.py task create \
  -v {PATH} \
  -t user.jodafons.Shenzhen.notuberculosis.model_wgangp.test_{TEST} \
  -c user.jodafons.job.Shenzhen.notuberculosis \
  -d user.jodafons.Shenzhen_table_from_raw.csv \
  --exec "{EXEC}" \
  --queue "gpu" \
  --bypass_local_test \
  """

try:
    os.makedirs(path)
except:
    pass

for test in range(10):
    cmd = command.format(PATH=path,EXEC=exec_cmd.format(TEST=test), TEST=test)
    print(cmd)
    os.system(cmd)
    break


