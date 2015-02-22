
(define else #t)
(define and (lambda (x . y)
    (cond ( (not x) #f)
        ((null? y) #t)
          (else (and (car y) (cdr y))))
    ))
(define or (lambda (x . y)
    (cond ( x #t)
        ((null? y) #f)
          (else (or (car y) (cdr y))))
    ))
(define last (lambda (y) (cond ( (null? (cdr y)) (car y)) (else (last (cdr y))))))
(define append (lambda (x y)
    (cond ( (null? x) y)
        (else (cons (car x) (append (cdr x) y))))))
(define list (lambda (x . y) (append (cons x '()) y)))
;; math stuff
(from-py-load 'operator 'add 'mul 'abs 'neg)
(define + (lambda (x y . z)
    (cond ((null? z) (add x y))
          (else (+ (add x y) (car z) (cdr z))))
    ))
(define * (lambda (x y . z)
    (cond ((null? z) (mul x y))
          (else (* (mul x y) (car z) (cdr z))))
    ))
(define - (lambda (x . y)
    (cond ((null? y) (neg x))
          ((null? (cdr y) )(+ x (neg (car y))))
          (else (- (+ x (neg (car y))) (cdr y) )))
    ))


;; the following does not work as expected since both "other" and
;; "if_true" would be evaluated
;(define if (lambda (test if_true other)
;    (cond (test if_true)
;          (else other))))
