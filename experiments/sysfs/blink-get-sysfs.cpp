#include <fcntl.h>
#include <unistd.h>
#include <assert.h>
#include <string.h>

#include <iostream>
#include <string>
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
        int fd = open("/sys/class/gpio/export", O_WRONLY);  // <--- man -s 2 open
        if (fd == -1) {                                     // <--- Unix error handling
            perror("open export file");
            return 1;                                       // <--- exit status 1
        }

        ssize_t nwritten = write(fd, GPIO, strlen(GPIO));   // <--- man -s 2 write
        if (nwritten == -1) {                               // <--- Unix error handling
            perror("write to export file");
            return 1;
        }

        close(fd);                                          // <--- man -s 2 close
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

    // get value
    // ---------
    //
    // $ cat /sys/class/gpio/gpio$GPIO/value
    {
        char filename[64];
        sprintf(filename, "/sys/class/gpio/gpio%s/value", GPIO);
        int fd = open(filename, O_RDONLY);
        assert(fd != -1);
        char value[2] = "x";
        ssize_t nread = read(fd, value, 1);                 // <--- man -s 2 read
        assert(nread == 1);

        cout << value << endl;
    }

    return 0;
}
