import boto
from boto.s3.key import Key
import time
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def S3Connection():
    connection = boto.connect_s3()
    return connection

def S3checker(connection,filename):
    start=time.time()
    bucket = connection.get_bucket('srirams3bucket')  
    key=Key(bucket)
    key.key=filename
    key.set_contents_from_filename(filename)
    time_taken = time.time()-start
    print 'It took ', time_taken, ' seconds'
    return time_taken

def filesizegenerator():
    return [x*1024*1024*5 for x in xrange(1,50)]

def filenamegenerator():
    return ['test'+str(i) for i in xrange(1,50)]

def create_file(path, size, generator=os.urandom):
    """Creates a file @ `path` of size in bytes `size` using
    a generator function `generator`. Generator must take a single
    argument, a size in bytes. By default, the generator is os.urandom.
    """
    with open(path, 'wb') as f:
        f.write(generator(size))

def filecreator():
    filenames= filenamegenerator()
    filesizes= filesizegenerator()
    actual_file_sizes = [filesize/(1024*1024) for filesize in filesizes]
    # for filename,filesize in zip(filenames,filesizes):
        # create_file(os.path.join(os.getcwd(),filename),filesize)

def get_throuhgput(actual_file_sizes,throughput_series):
    plt.clf()
    plt.plot(actual_file_sizes, throughput_series,label="File Sizes (in MB)  vs Throughput while uploading to S3 (in MB/s)")
    plt.xlabel("File Sizes in MB")
    plt.ylabel("Throughput in MB/s")
    plt.title("Upload Throughput difference with file size")
    plt.xlim(5, 250)
    plt.ylim(0, 50)
    plt.legend(loc="upper right")
    plt.savefig("S3_throughput.png")

def main():
    connection = S3Connection()
    time_taken_series = []
    throughput_series = []
    filecreator()
    filesizes= filesizegenerator()
    actual_file_sizes = [filesize/(1024*1024) for filesize in filesizes]
    filenames = filenamegenerator()
    for filename in filenames:
        time_taken_series.append(S3checker(connection,filename))
    for filesize,time in zip(actual_file_sizes,time_taken_series):
        throughput_series.append(float(filesize/time))
        print "Throughput was {0}".format(float(filesize/time))
    plt.plot(actual_file_sizes, time_taken_series,label="File Sizes (in MB)  vs Time taken to upload to S3 (in seconds)")
    plt.xlabel("File Sizes in MB")
    plt.ylabel("Time taken in seconds")
    plt.title("Upload Time difference with file size")
    plt.xlim(5, 250)
    plt.ylim(0, 50)
    plt.legend(loc="upper right")
    plt.savefig("S3_performance.png")
    get_throuhgput(actual_file_sizes,throughput_series)
if __name__ == '__main__':
    main()
