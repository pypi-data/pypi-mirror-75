# GridSearch-like on the grid
Searching good combinaisons of parameters happen quite ofter in ML-related task. I wrote a tool that help to achieve that. If you worked with the unix system call *fork*, you will see a similar approach with the API.

*The only requirement is jinja2*

## Hello World example
In this example we wrote all combinaisons of hello/hi world/Idiap.
```python
from easy_grid.experiences_manager import ExperienceBase

if __name__ == '__main__':
    if ExperienceBase.is_in_SGE(): # Write your task
        parameters = ExperienceBase.load_only_current()
        first = parameters['first']
        second = parameters['second']
        print('{} {}'.format(first, second))
    else: # Configure your task
        my_experience = ExperienceBase(python_executable='python3')
        my_experience.add_experience_key_values('first', ['hello', 'hi'])
        my_experience.add_experience_key_values('second', ['world', 'idiap'])

        my_experience.add_grid_parameter('-P', 'rise')
        my_experience.add_grid_parameter('-cwd', '')
        my_experience.add_grid_parameter('-N', 'hello_world')

        my_experience.add_export_parameter('PYTHONPATH', '.:$PYTHONPATH')

        my_experience.run(sync=True)
```
Run the example `python3 -m examples.hello_world` then check the results after running the script (and waiting a little bit)
`ls -1 output/hello_world.o*`
<pre>
output/hello_world.o5439319.1
output/hello_world.o5439319.2
output/hello_world.o5439319.3
output/hello_world.o5439319.4
</pre>
Each file contains the result of a combinaison. Let's check the content of the first one
`cat output/hello_world.o5439319.1`
> hello world

Get all results at once
`cat output/hello_world.o*`
<pre>
hello world
hi world
hello idiap
hi idiap
</pre>

## FizzBuzz example
We can also use task over a single parameter, like in fizzbuzz, which depend of *n*. Here an example with fizzbuzz from [1, 100]

```python
from easy_grid.experiences_manager import ExperienceBase

if __name__ == '__main__':
    if ExperienceBase.is_in_SGE(): # Write your task
        parameters = ExperienceBase.load_only_current()
        n = parameters['n']
        my_str = ''
        if n % 3 == 0: 
            my_str += 'Fizz'
        if n % 5 == 0: 
            my_str += 'Buzz'
        if my_str == '': 
            my_str = str(n)
        print('(n={:04d}) -> {}'.format(n, my_str))
    else: # Configure your task
        my_experience = ExperienceBase()
        my_experience.add_experience_key_values('n', list(range(1, 101)))

        my_experience.add_grid_parameter('-P', 'rise')
        my_experience.add_grid_parameter('-cwd', '')
        my_experience.add_grid_parameter('-N', 'fizzbuzz')

        my_experience.add_export_parameter('PYTHONPATH', '.:$PYTHONPATH')

        my_experience.run(sync=True)
```

Run the example `python3 -m examples.fizzbuzz`

Get all results at once and sort by n
`cat output/fizzbuzz.o* | sort`
<pre>
(n=0001) -> 1
(n=0002) -> 2
(n=0003) -> Fizz
(n=0004) -> 4
(n=0005) -> Buzz
(n=0006) -> Fizz
(n=0007) -> 7
(n=0008) -> 8
(n=0009) -> Fizz
(n=0010) -> Buzz
(n=0011) -> 11
...
(n=0090) -> FizzBuzz
(n=0091) -> 91
(n=0092) -> 92
(n=0093) -> Fizz
(n=0094) -> 94
(n=0095) -> Buzz
(n=0096) -> Fizz
(n=0097) -> 97
(n=0098) -> 98
(n=0099) -> Fizz
(n=0100) -> Buzz
</pre>

## Using with conda environment

You can use conda run with the python_executable parameter

```python
my_experience = ExperienceBase(python_executable="/idiap/user/wdroz/conda_stuff/miniconda3/condabin/conda run -n rise-baseline python3")
```
*you need to specify the full path of conda*