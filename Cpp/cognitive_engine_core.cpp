#include "cognitive_engine_core.hpp"
#include <iostream>
#include <sstream>
#include <ctime>
#include <regex>
#include <chrono>
#include <thread>

std::string CognitiveEngineCore::getCurrentTime() const {
    std::time_t now = std::time(nullptr);
    char buf[64];
    std::strftime(buf, sizeof(buf), "%Y-%m-%d %H:%M:%S", std::localtime(&now));
    return std::string(buf);
}

CognitiveEngineCore::CognitiveEngineCore() : loaded(false), introspectionLevel(1) {}

CognitiveEngineCore::~CognitiveEngineCore() {}

void CognitiveEngineCore::load() {
    std::lock_guard<std::mutex> lock(mtx);
    loaded = true;
    lastQueryTime = getCurrentTime();
    std::ostringstream oss;
    oss << "Cognitive Engine Core loaded successfully at " << lastQueryTime;
    sessionLog.push_back(oss.str());
    std::cout << oss.str() << std::endl;
}

std::string CognitiveEngineCore::processQuery(const std::string &query) {
    std::lock_guard<std::mutex> lock(mtx);
    lastQueryTime = getCurrentTime();
    sessionLog.push_back("Processed query: " + query);

    // Basic sentiment analysis.
    std::string sentiment = "neutral";
    std::regex positive("\\b(happy|joy|excellent|good)\\b", std::regex_constants::icase);
    std::regex negative("\\b(sad|bad|terrible|angry)\\b", std::regex_constants::icase);
    if (std::regex_search(query, positive))
        sentiment = "positive";
    else if (std::regex_search(query, negative))
        sentiment = "negative";

    // Check for deep-processing keywords.
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
    if (deepProcessing)
        oss << "Deep cognitive processing triggered.";
    else
        oss << "Standard processing applied.";
    std::string response = oss.str();
    std::cout << response << std::endl;
    return response;
}

std::future<std::string> CognitiveEngineCore::processQueryAsync(const std::string &query) {
    return std::async(std::launch::async, &CognitiveEngineCore::processQuery, this, query);
}

std::string CognitiveEngineCore::introspect() const {
    std::lock_guard<std::mutex> lock(mtx);
    std::ostringstream oss;
    oss << "System Introspection Report: ";
    if (!lastQueryTime.empty())
        oss << "Last query processed at " << lastQueryTime << ". ";
    else
        oss << "No queries processed yet. ";
    oss << "Introspection level: " << introspectionLevel << ".";
    std::string report = oss.str();
    std::cout << report << std::endl;
    return report;
}

void CognitiveEngineCore::reload() {
    {
        std::lock_guard<std::mutex> lock(mtx);
        std::cout << "Cognitive Engine Core reloading modules..." << std::endl;
        loaded = false;
    }
    std::this_thread::sleep_for(std::chrono::milliseconds(500));
    load();
}

bool CognitiveEngineCore::status() const {
    std::lock_guard<std::mutex> lock(mtx);
    return loaded;
}
