#include <iostream>

int main() {
    std::cout << "First 10 even numbers:" << std::endl;
    
    int count = 0;
    int number = 0;
    
    while (count < 10) {
        std::cout << number << std::endl;
        number += 2;
        count++;
    }
    
    return 0;
}