#include "DiffVisitor.hpp"
#include <unordered_map>
#include <iostream>
#include <slang/syntax/SyntaxTree.h>
#include <slang/syntax/SyntaxVisitor.h>
#include <filesystem>

namespace fs = std::filesystem;

struct PrinterVisitor: public SyntaxVisitor<PrinterVisitor> {
    template<typename T>
    void handle(const T& t) {
        // filter out tokens
        if constexpr (std::is_base_of_v<SyntaxNode, T>) {
            std::cout << t.kind << "\n";
        }
        visitDefault(t);
    }
};

int main(int argc, char* argv[]) {
    if(argc != 3) {
        std::cerr << "Invalid number of arguments provided. Aborting...\n";
        return 1;
    }

    std::unordered_map<std::string, int> res;
    DiffVisitor visitor{res, OP::SUB};

    std::string buggyFile {argv[1]};
    std::string fixedFile {argv[2]};

    // there are three scenarios:
    // 1) both files exist (modifications were made to the file)
    // 2) the buggy file does not exist (the file was created as part of the bug fix)
    // 3) the fixed file does not exist (the file was deleted as part of the bug fix)
    
    if(fs::exists(buggyFile) && fs::exists(fixedFile)) {
        // first parse and linearize the buggy file
        auto buggyTree = syntax::SyntaxTree::fromFile(buggyFile);
        if(buggyTree.has_value()) {
            buggyTree.value()->root().visit(visitor);
        }
        else {
            std::cerr << "Unable to parse file 1 (argv[2]). Aborting...\n";
            return 1;
        }

        // then parse and linearize the fixed file
        visitor.operation = OP::ADD;
        auto fixedTree = syntax::SyntaxTree::fromFile(fixedFile);
        // std::cout << argv[2] << std::endl;
        // std::cout << tree2->root().toString() << std::endl;;
        if(fixedTree.has_value()) {
            fixedTree.value()->root().visit(visitor);
        }
        else {
            std::cerr << "Unable to parse file 2 (argv[3]). Aborting...\n";
            return 1;
        }
    }
    else if (fs::exists(buggyFile)) {
        // first parse and linearize the buggy file
        auto buggyTree = syntax::SyntaxTree::fromFile(buggyFile);
        if(buggyTree.has_value()) {
            buggyTree.value()->root().visit(visitor);
        }
        else {
            std::cerr << "Unable to parse file 1 (argv[2]). Aborting...\n";
            return 1;
        }
    }
    else if (fs::exists(fixedFile)) {
        visitor.operation = OP::ADD;
        auto fixedTree = syntax::SyntaxTree::fromFile(std::string{fixedFile});
        // std::cout << argv[2] << std::endl;
        // std::cout << tree2->root().toString() << std::endl;;
        if(fixedTree.has_value()) {
            fixedTree.value()->root().visit(visitor);
        }
        else {
            std::cerr << "Unable to parse file 2 (argv[3]). Aborting...\n";
            return 1;
        }
    }

    for(auto & pair : res) {
        if(pair.second != 0) {
            std::cout << pair.first << ":" << pair.second <<"\n";
        }
    }
    return 0;
}