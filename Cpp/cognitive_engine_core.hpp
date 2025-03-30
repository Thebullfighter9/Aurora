#ifndef COGNITIVE_ENGINE_CORE_HPP
#define COGNITIVE_ENGINE_CORE_HPP

#include <string>
#include <vector>
#include <mutex>
#include <future>
#include <chrono>

class CognitiveEngineCore {
public:
    CognitiveEngineCore();
    ~CognitiveEngineCore();

    // Load (or initialize) the engine.
    void load();

    // Process a query synchronously and return a response string.
    std::string processQuery(const std::string &query);

    // Process a query asynchronously; returns a future.
    std::future<std::string> processQueryAsync(const std::string &query);

    // Return an introspection report.
    std::string introspect() const;

    // Simulate reloading the engine (clears and re-initializes state).
    void reload();

    // Return the current load status.
    bool status() const;

private:
    bool loaded;
    int introspectionLevel; // Higher value indicates deeper introspection.
    std::vector<std::string> sessionLog;
    std::chrono::system_clock::time_point lastQueryTime;
    mutable std::mutex mtx; // Protect shared resources.
};

#endif // COGNITIVE_ENGINE_CORE_HPP
