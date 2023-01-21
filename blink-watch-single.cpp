#include "utils.h"

#include <gpiod.h>

#include <sys/select.h>
#include <iostream>

using namespace std;


int main()
{
    gpiod_request_config *req_cfg = gpiod_request_config_new();
	gpiod_request_config_set_consumer(req_cfg, "blink-watch-single");

	gpiod_line_settings* settings = gpiod_line_settings_new();
    check_gpiod_error(gpiod_line_settings_set_direction(settings, GPIOD_LINE_DIRECTION_INPUT));
    check_gpiod_error(gpiod_line_settings_set_bias(settings, GPIOD_LINE_BIAS_PULL_UP));
    gpiod_line_settings_set_edge_detection(settings, GPIOD_LINE_EDGE_RISING);

    gpiod_line_config *line_cfg = gpiod_line_config_new();
    check_gpiod_error(gpiod_line_config_add_line_settings(line_cfg, &OFFSET, 1, settings));

    gpiod_chip* chip = gpiod_chip_open(DEVICE);
    assert(chip);

    gpiod_line_request *request = gpiod_chip_request_lines(chip, req_cfg, line_cfg);
    assert(request);

    int fd = gpiod_line_request_get_fd(request);    
    gpiod_edge_event_buffer* event_buffer = gpiod_edge_event_buffer_new(10);

    while (true) {
        fd_set in_fds;
        FD_ZERO(&in_fds);
        FD_SET(fd, &in_fds);

        int nready = select(fd+1, &in_fds, nullptr, nullptr, nullptr);
        assert(nready > 0);
        assert(FD_ISSET(fd, &in_fds));

        int nevents = gpiod_line_request_read_edge_events(request, event_buffer, 10);
        cout << "# Events: " << nevents << endl;

        for (int i=0; i<nevents; i++) {
            gpiod_edge_event* event = gpiod_edge_event_buffer_get_event(event_buffer, i);

            gpiod_edge_event_type type = gpiod_edge_event_get_event_type(event);
            uint64_t timestamp = gpiod_edge_event_get_timestamp_ns(event);
            unsigned int offset = gpiod_edge_event_get_line_offset(event);
            unsigned long global_seqno = gpiod_edge_event_get_global_seqno(event);
            unsigned long line_seqno = gpiod_edge_event_get_line_seqno(event);

            cout << "  Type: " << event_type_str(type) << endl;
            cout << "  Timestamp: " << timestamp << endl;
            cout << "  Offset: " << offset << endl;
            cout << "  Global seqno: " << global_seqno << endl;
            cout << "  Line seqno: " << line_seqno << endl;
        }
    }

    gpiod_edge_event_buffer_free(event_buffer);
    gpiod_line_request_release(request);
    gpiod_line_config_free(line_cfg);
    gpiod_line_settings_free(settings);
    gpiod_chip_close(chip);

    return 0;
}
