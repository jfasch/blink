#pragma once

#include <gpiod.h>
#include <assert.h>
#include <string>

static const char DEVICE[] = "/dev/gpiochip0";
static const unsigned OFFSET = 26;

#define check_gpiod_error(err) assert(err!=-1)

static inline const char* event_type_str(gpiod_edge_event_type type)
{
    switch (type) {
        case GPIOD_EDGE_EVENT_RISING_EDGE:
            return "rising";
        case GPIOD_EDGE_EVENT_FALLING_EDGE:
            return "falling";
    }
    assert(!"bad event type");
    return "bad";
}

static inline gpiod_line_value str_to_line_value(const std::string& s)
{
    if (s == "1" || s == "true")
        return GPIOD_LINE_VALUE_ACTIVE;
    else if (s == "0" || s == "false")
        return GPIOD_LINE_VALUE_INACTIVE;
    else {
        assert(!"bad boolean value");
        return GPIOD_LINE_VALUE_ERROR;
    }
}
