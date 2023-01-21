#include "utils.h"

#include <gpiod.h>

#include <unistd.h>
#include <string>

#include <chrono>
#include <thread>
#include <iostream>
using namespace std;
using namespace std::literals::chrono_literals;


const unsigned int OFFSETS[] = {
    /*0*/ 19,
    /*1*/ 13,
    /*2*/  6,
    /*3*/  5,
    /*4*/ 22,
    /*5*/ 27,
    /*6*/ 17,
    /*7*/ 21,
};
const unsigned int NOFFSETS = sizeof(OFFSETS)/sizeof(int);

int main(int argc, char** argv)
{
    gpiod_request_config *req_cfg = gpiod_request_config_new();
    gpiod_request_config_set_consumer(req_cfg, "blink-kitt");

	gpiod_line_settings* settings = gpiod_line_settings_new();
    check_gpiod_error(gpiod_line_settings_set_direction(settings, GPIOD_LINE_DIRECTION_OUTPUT));
    check_gpiod_error(gpiod_line_settings_set_bias(settings, GPIOD_LINE_BIAS_DISABLED));

    gpiod_line_config *line_cfg = gpiod_line_config_new();
    check_gpiod_error(gpiod_line_config_add_line_settings(line_cfg, OFFSETS, NOFFSETS, settings));

    gpiod_chip* chip = gpiod_chip_open(DEVICE);
    assert(chip);

    gpiod_line_request *request = gpiod_chip_request_lines(chip, req_cfg, line_cfg);
    assert(request);

    int index = 0;
    int movement = +1;
    while (true) {
        check_gpiod_error(gpiod_line_request_set_value(request, OFFSETS[index], line_value(true)));
        this_thread::sleep_for(0.06s);
        check_gpiod_error(gpiod_line_request_set_value(request, OFFSETS[index], line_value(false)));
        
        if (index == NOFFSETS-1)
            movement = -1;
        else if (index == 0)
            movement = +1;

        index += movement;
    }
 
    return 0;
}
