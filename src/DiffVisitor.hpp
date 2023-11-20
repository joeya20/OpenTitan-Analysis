#include <memory>
#include <queue>
#include <slang/parsing/Token.h>
#include <slang/syntax/SyntaxTree.h>
#include <slang/syntax/SyntaxVisitor.h>
#include <slang/syntax/AllSyntax.h>
#include <slang/syntax/SyntaxKind.h>
#include <type_traits>
#include <unordered_map>
#include <string>
#include <sstream>
#include <iostream>
#include <vector>

using namespace slang;
using namespace syntax;

struct SearchVisitor: public SyntaxVisitor<SearchVisitor> {
    std::vector<const SyntaxNode*> linearTree;
    SearchVisitor(std::shared_ptr<SyntaxTree> tree) {
        std::queue<const SyntaxNode*> jobQ;
        linearTree.push_back(&tree->root());
        jobQ.push(&tree->root());
        while (jobQ.size() > 0) {
            auto currNode = jobQ.front();
            jobQ.pop();
            
            for(size_t i = 0; i < currNode->getChildCount(); i++) {
                auto child = currNode->childNode(i);
                if(!child) continue;
                jobQ.push(child);
                linearTree.push_back(child);
            }
        }
    }
};

enum OP {ADD, SUB};
struct DiffVisitor: public SyntaxVisitor<DiffVisitor> {
    std::unordered_map<std::string, int>& res;
    enum OP operation;
    DiffVisitor(std::unordered_map<std::string, int>& res, enum OP op) :  res(res) {
        operation = op;
    }

    template<typename T>
    void handle(const T& t) {
        if constexpr (std::is_base_of_v<MemberSyntax, T> || 
        std::is_base_of_v<StatementSyntax, T>) {
            std::stringstream ss;
            ss << t.kind;
            if (operation == ADD) {
                res[ss.str()]++;
            }
            else {
                res[ss.str()]--;
            }
        }
        else if (std::is_base_of_v<ExpressionSyntax, T> && (    // assignments and ternary operator
            t.kind == SyntaxKind::AssignmentExpression ||
            t.kind == SyntaxKind::AddAssignmentExpression ||
            t.kind == SyntaxKind::SubtractAssignmentExpression ||
            t.kind == SyntaxKind::MultiplyAssignmentExpression ||
            t.kind == SyntaxKind::DivideAssignmentExpression ||
            t.kind == SyntaxKind::ModAssignmentExpression ||
            t.kind == SyntaxKind::AndAssignmentExpression ||
            t.kind == SyntaxKind::OrAssignmentExpression ||
            t.kind == SyntaxKind::XorAssignmentExpression ||
            t.kind == SyntaxKind::LogicalLeftShiftAssignmentExpression ||
            t.kind == SyntaxKind::LogicalRightShiftAssignmentExpression ||
            t.kind == SyntaxKind::ArithmeticLeftShiftAssignmentExpression ||
            t.kind == SyntaxKind::ArithmeticRightShiftAssignmentExpression ||
            t.kind == SyntaxKind::NonblockingAssignmentExpression ||
            t.kind == SyntaxKind::ConditionalExpression
        )) {
            std::stringstream ss;
            ss << t.kind;
            if (operation == ADD) {
                res[ss.str()]++;
            }
            else {
                res[ss.str()]--;
            }
        }
        visitDefault(t);
    }

    bool hasMatchingNode(const SyntaxNode& node) {
        
    }
};
