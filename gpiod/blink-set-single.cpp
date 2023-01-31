#include "utils.h"

#include <gpiod.h>

#include <unistd.h>
#include <string>
#include <iostream>
using namespace std;

int main(int argc, char** argv)
{
    if (argc < 3) {
        cerr << "Usage: " << argv[0] << " <GPIO#> <value> [<hold-time-sec>]"<< endl;
        return 1;
    }

    unsigned int offset = stoul(argv[1]);
    gpiod_line_value value = line_value(argv[2]);
    unsigned int hold_time_sec = -1;
    if (argc == 4)
        hold_time_sec = stoul(argv[3]);
    
    gpiod_request_config *req_cfg = gpiod_request_config_new();
	gpiod_request_config_set_consumer(req_cfg, "blink-set-single");

	gpiod_line_settings* settings = gpiod_line_settings_new();
    check_gpiod_error(gpiod_line_settings_set_direction(settings, GPIOD_LINE_DIRECTION_OUTPUT));
    check_gpiod_error(gpiod_line_settings_set_bias(settings, GPIOD_LINE_BIAS_DISABLED));

    gpiod_line_config *line_cfg = gpiod_line_config_new();
    check_gpiod_error(gpiod_line_config_add_line_settings(line_cfg, &offset, 1, settings));

    gpiod_chip* chip = gpiod_chip_open(DEVICE);
    assert(chip);

    gpiod_line_request *request = gpiod_chip_request_lines(chip, req_cfg, line_cfg);
    assert(request);

    check_gpiod_error(gpiod_line_request_set_value(request, offset, value));
   
    if (hold_time_sec > 0)
        sleep(hold_time_sec);
    else
        pause();
 
    return 0;
}
