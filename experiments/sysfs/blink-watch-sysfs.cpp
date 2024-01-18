#include <fcntl.h>
#include <unistd.h>
#include <assert.h>
#include <string.h>
#include <sys/select.h>

#include <iostream>
using namespace std;

int main(int argc, char** argv)
{
    if (argc != 2) {
        cerr << "Usage: " << argv[0] << " <GPIO#>" << endl;
        return 1;
    }

    const char* GPIO = argv[1];
    stoi(GPIO); // check if GPIO is int

    // export GPIO
    // -----------
    //
    // $ echo $GPIO > /sys/class/gpio/export
    {
        int fd = open("/sys/class/gpio/export", O_WRONLY);
        if (fd == -1) {
            perror("open export file");
            return 1;
        }

        ssize_t nwritten = write(fd, GPIO, strlen(GPIO));
        if (nwritten == -1) {
            perror("write to export file");
            return 1;
        }

        close(fd);
    }

    // give system time to export GPIO (sadly, this is an asynchronous
    // operation)
    sleep(1);

    // configure GPIO as input
    // -----------------------
    //
    // $ echo in > /sys/class/gpio/gpio$GPIO/direction
    {
        char filename[64];
        sprintf(filename, "/sys/class/gpio/gpio%s/direction", GPIO);
        int fd = open(filename, O_WRONLY);
        ssize_t nwritten = write(fd, "in", 2);
        if (nwritten == -1) {
            perror("configure direction");
            return 2;
        }
        assert(nwritten == 2);
        close(fd);
    }

    // edge detection: "rising"
    // ------------------------
    // 
    // $ echo rising > /sys/class/gpio/gpio$GPIO/direction/edge
    {
        char filename[64];
        sprintf(filename, "/sys/class/gpio/gpio%s/edge", GPIO);
        int fd = open(filename, O_WRONLY);
        ssize_t nwritten = write(fd, "rising", 6);
        if (nwritten == -1) {
            perror("configure edge");
            return 3;
        }
        assert(nwritten == 6);
        close(fd);
    }

    // wait for value to change
    // ------------------------
    {
        char filename[64];
        sprintf(filename, "/sys/class/gpio/gpio%s/value", GPIO);
        int fd = open(filename, O_RDONLY);
        assert(fd != -1);

        while (true) {
            fd_set exc_fds;
            FD_ZERO(&exc_fds);
            FD_SET(fd, &exc_fds);

            int nready = select(fd+1, nullptr, nullptr, &exc_fds, nullptr);
            if (nready == -1) {
                perror("select");
                return 4;
            }
            assert(nready > 0);

            if (FD_ISSET(fd, &exc_fds)) {
                char value[2] = "x";
                ssize_t nread = read(fd, value, 1);
                if (nread == -1) {
                    perror("read value");
                    return 5;
                }

                off_t off = lseek(fd, 0, SEEK_SET);
                if (off == -1) {
                    perror("lseek");
                    return 6;
                }

                cout << "EEK:" << value << endl;
            }
        }
    }

    return 0;
}
