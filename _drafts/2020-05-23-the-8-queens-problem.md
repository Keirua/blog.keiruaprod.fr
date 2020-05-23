solving the 8 queens problem.md

The 8 queens problem is a popular problem that lends itself very well to backtracking.

When you are studying computer science, implementing is often one of the exercises that help you understand.

Unfortunately, it also has a [closed-form solution](https://en.wikipedia.org/wiki/Eight_queens_puzzle#Solutions) that spoils all the fun.

```python
import random

def generate_queens(n):
    positions = []
    if ((n%2 == 0) and (n%6==2)):
        for i in range(1, n/2+1):
            positions.append([i, 2*i])
            positions.append([n/2+i, 2*i-1])
    return positions
    

def draw_board(positions, n):
    board = []
    empty_line = [' ' for i in range(n) ]
    board = [list(empty_line) for i in range(n) ]
    for p in positions:
        board[p[0]-1][p[1]-1] = '*'
    for i in range(n):
        print(board[i])

def is_valid(positions):
    for p in positions:
        for c in [x for x in positions if x != p]:
            if p[0] == c[0] or p[1] == c[1] or abs(p[0]-c[0])==abs(p[1]-c[1]):
                return False
        print(p)
    return True

n = 8;
queens = generate_queens(n)
print(queens)
print("Board:")
draw_board(queens, n)

print(is_valid(queens))
```

Here is another solution using the same algorithm, this time in Rust:

```rust
use std::fmt;

#[derive(Debug)]
struct Position {
    x:i32,
    y:i32
}

fn generate_queens(n:i32) -> Vec<Position>{
    let mut positions:Vec<Position> = Vec::new();

    if (n % 2 == 0) && (n %6 == 2) {
        for i in 1..n/2+1 {
            positions.push(Position{
                x: i,
                y: 2*i
            });
            positions.push(Position{
                x: n/2+i,
                y: 2*i-1
            });
        }
    }

    positions
}

#[derive(Debug)]
pub struct Board {
    queens: Vec<Position>
}

impl Board {
    pub fn new(n: i32) -> Board {
        Board{
            queens:generate_queens(n)
        }
    }
}

impl fmt::Display for Board {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        let size = self.queens.len() as i32;
        for i in 0..size {
            for j in 0..size {
                let mut has_queen = false;
                for q in self.queens.iter() {
                    if q.x-1 ==i && q.y-1 == j {
                        let _ = write!(f, "♛");
                        has_queen = true;
                        break;
                    }
                }
                if !has_queen {
                    let _ = write!(f, ".");
                }
            }
            let _ = write!(f, "\n");
        }
        write!(f, "")
    }
}

fn main() {
    let board = Board::new(8);
    println!("{:#?}", board);
    println!("{}", board);
}
```