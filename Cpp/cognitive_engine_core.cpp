#include "cognitive_engine_core.hpp"
#include <sstream>
#include <ctime>
#include <chrono>
#include <thread>
#include <iostream>
#include <regex>
#include <random>

CognitiveEngineCore::CognitiveEngineCore() 
    : loaded(false), cycleCount(0), currentTopic("Default Research Topic") {
    addDebug("Cognitive Engine Core instance created.");
    researchTopicsPool = {"Coding", "Games", "Science", "Math", "History", 
                          "Philosophy", "Literature", "Music", "Art", "Technology"};
}

CognitiveEngineCore::~CognitiveEngineCore() {
    addDebug("Cognitive Engine Core shutting down.");
}

std::string CognitiveEngineCore::getCurrentTime() const {
    std::time_t now = std::time(nullptr);
    char buf[64];
    std::strftime(buf, sizeof(buf), "%Y-%m-%d %H:%M:%S", std::localtime(&now));
    return std::string(buf);
}

void CognitiveEngineCore::addDebug(const std::string &entry) const {
    std::lock_guard<std::mutex> lock(mtx);
    std::string logEntry = getCurrentTime() + " - " + entry;
    debugLog.push_back(logEntry);
    std::cout << logEntry << std::endl;
}

void CognitiveEngineCore::load() {
    std::lock_guard<std::mutex> lock(mtx);
    loaded = true;
    cycleCount = 0;
    currentTopic = "Default Research Topic";
    addDebug("Cognitive Engine Core loaded successfully at " + getCurrentTime());
}

std::string CognitiveEngineCore::processQuery(const std::string &query) {
    std::lock_guard<std::mutex> lock(mtx);
    cycleCount++;
    addDebug("Processed query: " + query);

    // Basic sentiment analysis using regex.
    std::string sentiment = "neutral";
    std::regex positive("\\b(happy|joy|excellent|good)\\b", std::regex_constants::icase);
    std::regex negative("\\b(sad|bad|terrible|angry)\\b", std::regex_constants::icase);
    if (std::regex_search(query, positive)) {
        sentiment = "positive";
    } else if (std::regex_search(query, negative)) {
        sentiment = "negative";
    }

    // Check for custom keywords triggering deep processing.
    bool deepProcessing = false;
    std::vector<std::string> keywords = {"synergy", "conscious", "adaptive", "self-aware"};
    for (const auto &keyword : keywords) {
        if (query.find(keyword) != std::string::npos) {
            deepProcessing = true;
            break;
        }
    }

    std::ostringstream oss;
    oss << "Query: '" << query << "' processed. Detected sentiment: " << sentiment << ". ";
    oss << (deepProcessing ? "Deep cognitive processing triggered." : "Standard processing applied.");
    std::string response = oss.str();
    addDebug(response);
    return response;
}

std::future<std::string> CognitiveEngineCore::processQueryAsync(const std::string &query) {
    return std::async(std::launch::async, &CognitiveEngineCore::processQuery, this, query);
}

std::string CognitiveEngineCore::introspect() const {
    std::lock_guard<std::mutex> lock(mtx);
    std::ostringstream oss;
    oss << "System Introspection Report: ";
    oss << "Last query processed at " << getCurrentTime() << ". ";
    oss << "Introspection level: 1.";
    std::string report = oss.str();
    addDebug(report);  // Now allowed in a const method
    return report;
}

void CognitiveEngineCore::reload() {
    {
        std::lock_guard<std::mutex> lock(mtx);
        addDebug("Cognitive Engine Core reloading modules...");
        loaded = false;
    }
    std::this_thread::sleep_for(std::chrono::milliseconds(500)); // Simulate delay.
    load();
}

bool CognitiveEngineCore::status() const {
    std::lock_guard<std::mutex> lock(mtx);
    return loaded;
}

void CognitiveEngineCore::setResearchTopic(const std::string &topic) {
    std::lock_guard<std::mutex> lock(mtx);
    currentTopic = topic;
    addDebug("Research topic set to: " + currentTopic);
}

std::string CognitiveEngineCore::performResearchCycle() {
    std::lock_guard<std::mutex> lock(mtx);
    cycleCount++;
    std::ostringstream oss;
    oss << "Cycle " << cycleCount << " completed. Researching topic: " << currentTopic;
    addDebug(oss.str());
    std::this_thread::sleep_for(std::chrono::milliseconds(500)); // Simulate research delay.
    return oss.str();
}

void CognitiveEngineCore::continuousResearch(int cycles) {
    addDebug("Entering continuous research mode.");
    for (int i = 0; i < cycles; i++) {
        setResearchTopic(selectRandomTopic());
        performResearchCycle();
    }
    addDebug("Exiting continuous research mode.");
}

std::string CognitiveEngineCore::getDebugLog() const {
    std::lock_guard<std::mutex> lock(mtx);
    std::ostringstream oss;
    for (const auto &entry : debugLog) {
        oss << entry << "\n";
    }
    return oss.str();
}

int CognitiveEngineCore::getCycleCount() const {
    std::lock_guard<std::mutex> lock(mtx);
    return cycleCount;
}

std::string CognitiveEngineCore::selectRandomTopic() {
    if (researchTopicsPool.empty())
        return "General Research";
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<> dis(0, researchTopicsPool.size() - 1);
    return researchTopicsPool[dis(gen)];
}

#ifdef TEST_ENGINE
// Test main function. Remove or guard this when integrating with Python.
#include <iostream>
int main() {
    CognitiveEngineCore engine;
    engine.load();
    std::cout << engine.processQuery("I am very happy today!") << std::endl;
    auto asyncResp = engine.processQueryAsync("Testing synergy in deep processing.");
    std::cout << asyncResp.get() << std::endl;
    std::cout << engine.introspect() << std::endl;
    engine.setResearchTopic("Quantum Computing");
    engine.performResearchCycle();
    engine.continuousResearch(5);
    std::cout << "Debug Log:\n" << engine.getDebugLog() << std::endl;
    engine.reload();
    std::cout << "Engine status: " << (engine.status() ? "Loaded" : "Not loaded") << std::endl;
    return 0;
}
#endif
