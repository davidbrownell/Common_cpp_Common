#define CATCH_CONFIG_MAIN  // This tells Catch to provide a main() - only do this in one cpp file
#define CATCH_CONFIG_CONSOLE_WIDTH 200
#include <catch.hpp>

#include "lib.h"

TEST_CASE("Standard") {
    CHECK(Func() == std::vector<std::string>{"one", "two", "three"});
}
