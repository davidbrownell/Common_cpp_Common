#define CATCH_CONFIG_MAIN  // This tells Catch to provide a main() - only do this in one cpp file
#define CATCH_CONFIG_CONSOLE_WIDTH 200
#include <catch.hpp>

#include "shared.h"

TEST_CASE("Standard") {
    StringData *                            pStringData(nullptr);
    size_t                                  cStringData(0);

    CHECK(InvokeFunc(&pStringData, &cStringData));
    REQUIRE(pStringData != nullptr);
    REQUIRE(cStringData == 3);

    CHECK(strcmp(pStringData[0].pStringData, "one") == 0);
    CHECK(pStringData[0].cStringData == 3);

    CHECK(strcmp(pStringData[1].pStringData, "two") == 0);
    CHECK(pStringData[1].cStringData == 3);

    CHECK(strcmp(pStringData[2].pStringData, "three") == 0);
    CHECK(pStringData[2].cStringData == 5);

    CHECK(DeleteStringData(pStringData, cStringData));
}
