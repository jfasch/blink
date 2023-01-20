#include "utils.h"

#include <gpiod.h>

#include <iostream>
using namespace std;

int main()
{
    gpiod_request_config *req_cfg = gpiod_request_config_new();
	gpiod_request_config_set_consumer(req_cfg, "blink-get");

	gpiod_line_settings* settings = gpiod_line_settings_new();
    check_gpiod_error(gpiod_line_settings_set_direction(settings, GPIOD_LINE_DIRECTION_INPUT));
    check_gpiod_error(gpiod_line_settings_set_bias(settings, GPIOD_LINE_BIAS_PULL_UP));

    gpiod_line_config *line_cfg = gpiod_line_config_new();
    check_gpiod_error(gpiod_line_config_add_line_settings(line_cfg, &OFFSET, 1, settings));

    gpiod_chip* chip = gpiod_chip_open(DEVICE);
    assert(chip);

    gpiod_line_request *request = gpiod_chip_request_lines(chip, req_cfg, line_cfg);
    assert(request);

    gpiod_line_value value = gpiod_line_request_get_value(request, OFFSET);
    check_gpiod_error(value);

    cout << value << endl;
    
    gpiod_line_request_release(request);
    gpiod_line_config_free(line_cfg);
    gpiod_line_settings_free(settings);
    gpiod_chip_close(chip);

    return 0;
}
