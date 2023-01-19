#pragma once

#include <gpiod.h>
#include <assert.h>

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
 
