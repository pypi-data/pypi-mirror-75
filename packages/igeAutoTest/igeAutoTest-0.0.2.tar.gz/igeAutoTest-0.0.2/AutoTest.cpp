#include "AutoTest.h"
#include "AutoTestImpl.h"
#include <fstream>

#if !BUILD_EXTENSION
#include "Adj.h"
#include "SDL.h"
#include "GAnalytics.h"
#include "AdsApplovin.h"
extern SDL_bool SDL_IsGameLoopTest();
#endif

#if defined _WIN32              //WIN32
#   include <time.h>
#   include <windows.h>
#elif defined __APPLE__
#   include "TargetConditionals.h"
#   if TARGET_OS_IPHONE        //iOS
#       include <sys/types.h>
#   else                       //OSX
#       include <time.h>
#   endif
#	include <mach/mach_time.h>
#elif defined __ANDROID__       //Android
#   include <sys/time.h>
#   include <time.h>
#endif

namespace autotest
{
    static double GetCPUTime() {
#if defined _WIN32
        static LARGE_INTEGER	cuurentTime;
        static LARGE_INTEGER	freq;

        QueryPerformanceCounter(&cuurentTime);
        QueryPerformanceFrequency(&freq);
        return (double)cuurentTime.QuadPart / (double)freq.QuadPart;
#elif defined __ANDROID__
        struct timespec tv;
        clock_gettime(CLOCK_MONOTONIC, &tv);
        return (double)tv.tv_sec + (double)tv.tv_nsec / 1000000000.0;
#else
        static mach_timebase_info_data_t base;
        mach_timebase_info(&base);

        uint64_t t = mach_absolute_time();
        double tsec = (double)t * (double)base.numer / (double)base.denom / 1000000000.0;
        return tsec;
#endif
    }
}

AutoTest* AutoTest::instance = nullptr;

AutoTest::AutoTest()
    : m_autoTestImpl(new AutoTestImpl())
{

}

AutoTest::~AutoTest()
{
}

void AutoTest::collectModuleInfo()
{
    adjustInfo();
    gameAnalyticsInfo();
    applovinInfo();
}

void AutoTest::adjustInfo()
{
#if BUILD_EXTENSION
    result_json["Adjust"] = {};
#else
    Adj* adjust = Adj::Instance();

    json jAdjust = adjust->dumpInfo();
    result_json["Adjust"] = jAdjust;
#endif
}

void AutoTest::gameAnalyticsInfo()
{
#if BUILD_EXTENSION
    result_json["GameAnalytics"] = {};
#else
    GAnalytics* ga = GAnalytics::Instance();
    json jGA = ga->dumpInfo();;
    
    result_json["GameAnalytics"] = jGA;
#endif
}

void AutoTest::applovinInfo()
{
#if BUILD_EXTENSION
    result_json["Applovin"] = {};
#else
    AdsApplovin* applovin = AdsApplovin::Instance();
    json jApplovin = applovin->dumpInfo();;

    result_json["Applovin"] = jApplovin;
#endif
}

void AutoTest::finishLoop()
{
    if(GetImpl() != nullptr)
    {
        collectModuleInfo();
        
        writeResults("Result", "Success");
        
        const char* path = GetImpl()->GetResultPath();
        std::ofstream file(path);
        file << result_json;
        
        printf("%s", result_json.dump(4).c_str());
        GetImpl()->FinishLoop();
    }
}

void AutoTest::writeResults(const char* name, const char* value)
{
    result_json.emplace(name, value);
}

void AutoTest::writeResults(const char* name, int value)
{
    result_json.emplace(name, value);
}

void AutoTest::screenshots()
{
    if(GetImpl() != nullptr)
    {        
        GetImpl()->Screenshots(std::to_string(autotest::GetCPUTime()).c_str());
    }
}

bool AutoTest::isLoopTest()
{
#if BUILD_EXTENSION
    return false;
#else
    return (SDL_IsGameLoopTest() == SDL_TRUE);
#endif
}
