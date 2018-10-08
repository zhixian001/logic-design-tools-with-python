# logic-design-tools-with-python
logic-design-tools-with-python

## input.json 

multiple expressions available

1. expression: boolean expression
2. not-shown: elements that is not shown in boolean expression
3. order: 1 -> decreasing / 0 -> increasing
4. dont-cares: input combinations that won't care. * is wildcard.
### example
```json
{
    "F1" : [{
        "expression": "a1*(a3^a4)",
        "not-shown": [
            "a2",
            "a5"
        ],
        "order": 1,
        "dont-cares" : [
            "00101",
            "*1*0*"
        ],
    }],
    "F0" : [{
        "expression": "a5*(a3|a4)",
        "not-shown": [
            "a2",
            "a3"
        ],
        "order": 0,
        "dont-cares" : [
            "00101",
            "*1*0*"
        ],
    }]
}
```

## Known Issue

- JSON Expression should be separated with '(' ')' and proper spaces. Unless result is incorrect
