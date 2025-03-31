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

    // Set a specific research topic.
    void setResearchTopic(const std::string &topic);

    // Performs one research cycle (simulated).
    std::string performResearchCycle();

    // Runs continuous research mode for a given number of cycles.
    void continuousResearch(int cycles = 10);

    // Retrieves the debug log.
    std::string getDebugLog() const;

    // Returns the number of research cycles completed.
    int getCycleCount() const;

private:
    bool loaded;
    int cycleCount;
    std::string currentTopic;

    // Mark debugLog and mutex as mutable so they can be modified in const methods.
    mutable std::vector<std::string> debugLog;
    mutable std::mutex mtx;

    // Returns the current time as string "YYYY-MM-DD HH:MM:SS".
    std::string getCurrentTime() const;

    // Append a new entry to the debug log (now a const method).
    void addDebug(const std::string &entry) const;

    // Selects a random topic from the pool.
    std::string selectRandomTopic();

    // Pool of topics for auto research.
    std::vector<std::string> researchTopicsPool;
};

#endif // COGNITIVE_ENGINE_CORE_HPP
