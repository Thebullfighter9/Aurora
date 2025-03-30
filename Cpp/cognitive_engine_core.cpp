#include "cognitive_engine_core.hpp"
#include <iostream>
#include <sstream>
#include <regex>
#include <thread>
#include <future>
#include <chrono>
#include <ctime>

CognitiveEngineCore::CognitiveEngineCore()
    : loaded(false), introspectionLevel(1)
{
    // Constructor: Initialization can be performed later via load()
}

CognitiveEngineCore::~CognitiveEngineCore() {
    // Destructor (if any cleanup is needed)
}

void CognitiveEngineCore::load() {
    std::lock_guard<std::mutex> lock(mtx);
    loaded = true;
    lastQueryTime = std::chrono::system_clock::now();
    sessionLog.push_back("Cognitive Engine Core initialized.");
    // Log initialization with a timestamp.
    std::time_t now = std::chrono::system_clock::to_time_t(lastQueryTime);
    std::cout << std::ctime(&now) << " Cognitive Engine Core loaded successfully." << std::endl;
}

std::string CognitiveEngineCore::processQuery(const std::string &query) {
    std::lock_guard<std::mutex> lock(mtx);
    lastQueryTime = std::chrono::system_clock::now();
    sessionLog.push_back("Processed query: " + query);

    // Basic sentiment analysis (using regex).
    std::string sentiment = "neutral";
    std::regex positive("\\b(happy|joy|excellent|good)\\b", std::regex_constants::icase);
    std::regex negative("\\b(sad|bad|terrible|angry)\\b", std::regex_constants::icase);
    if (std::regex_search(query, positive)) {
        sentiment = "positive";
    } else if (std::regex_search(query, negative)) {
        sentiment = "negative";
    }

    // Build the response message.
    std::ostringstream response;
    response << "Query: '" << query << "' processed. Detected sentiment: " << sentiment << ". ";
    
    // Trigger deeper processing if custom keywords are detected.
    if (query.find("synergy") != std::string::npos ||
        query.find("conscious") != std::string::npos ||
        query.find("adaptive") != std::string::npos ||
        query.find("self-aware") != std::string::npos)
    {
        response << "Deep cognitive processing triggered.";
    } else {
        response << "Standard processing applied.";
    }

    // Log the response.
    std::cout << response.str() << std::endl;
    return response.str();
}

std::future<std::string> CognitiveEngineCore::processQueryAsync(const std::string &query) {
    // Launch asynchronous processing.
    return std::async(std::launch::async, &CognitiveEngineCore::processQuery, this, query);
}

std::string CognitiveEngineCore::introspect() const {
    std::lock_guard<std::mutex> lock(mtx);
    std::ostringstream report;
    report << "System Introspection Report: ";
    if (lastQueryTime.time_since_epoch().count() != 0) {
        std::time_t lastTime = std::chrono::system_clock::to_time_t(lastQueryTime);
        report << "Last query processed at " << std::ctime(&lastTime);
    } else {
        report << "No queries processed yet. ";
    }
    report << "Introspection level: " << introspectionLevel << ".";
    std::cout << report.str() << std::endl;
    return report.str();
}

void CognitiveEngineCore::reload() {
    {
        std::lock_guard<std::mutex> lock(mtx);
        std::cout << "Reloading Cognitive Engine Core modules..." << std::endl;
        loaded = false;
    }
    // Simulate reload delay.
    std::this_thread::sleep_for(std::chrono::milliseconds(500));
    load();
}

bool CognitiveEngineCore::status() const {
    std::lock_guard<std::mutex> lock(mtx);
    return loaded;
}
