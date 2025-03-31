#ifndef COGNITIVE_ENGINE_CORE_HPP
#define COGNITIVE_ENGINE_CORE_HPP

#include <string>
#include <vector>
#include <mutex>
#include <future>

class CognitiveEngineCore {
public:
    CognitiveEngineCore();
    ~CognitiveEngineCore();

    // Loads (initializes) the cognitive engine.
    void load();

    // Processes a query synchronously and returns a response string.
    std::string processQuery(const std::string &query);

    // Processes a query asynchronously.
    std::future<std::string> processQueryAsync(const std::string &query);

    // Returns an introspection report.
    std::string introspect() const;

    // Reloads the cognitive engine (simulated).
    void reload();

    // Returns the current load status.
    bool status() const;

private:
    bool loaded;
    std::vector<std::string> sessionLog;
    int introspectionLevel;
    std::string lastQueryTime;
    mutable std::mutex mtx;

    // Helper function: returns current time as string "YYYY-MM-DD HH:MM:SS".
    std::string getCurrentTime() const;
};

#endif // COGNITIVE_ENGINE_CORE_HPP
