import sys
from typing import NamedTuple, List, Tuple, Dict, Optional
from linkedin.smart_arg import arg_suite


# Define the argument
@arg_suite
class MyArg(NamedTuple):
    """
    MyArg is smart! (docstring goes to description)
    """
    nn: List[int]  # Comments go to argparse help
    a_tuple: Tuple[str, int]  # a random tuple argument
    encoder: str  # Text encoder type
    h_param: Dict[str, int]  # Hyperparameters
    batch_size: Optional[int] = None
    adp: bool = True  # bool is a bit tricky
    embedding_dim: int = 100  # Size of embedding vector
    lr: float = 1e-3  # Learning rate


def cli_interfaced_job_scheduler():
    # Create the argument instance
    my_arg = MyArg(nn=[3], a_tuple=("str", 1), encoder='lstm', h_param={}, adp=False)  # The patched argument class requires keyword arguments to instantiate the class

    # Serialize the argument to command-line representation
    argv = my_arg.__to_argv__()
    cli = 'my_job.py ' + ' '.join(argv)
    # Schedule the job with command line `cli`
    print(f"Executing job:\n{cli}")
    # Executing job:
    # my_job.py --nn 3 --a_tuple str 1 --encoder lstm --h_param --batch_size None --adp False --embedding_dim 100 --lr 0.001


# my_job.py
def main():
    # Deserialize the command-line representation of the argument back to an instance
    my_arg: MyArg = MyArg.__from_argv__(sys.argv[1:])  # Equivalent to `MyArg(None)`, one positional arg required to indicate the arg is a command-line representation.
    print(my_arg)
    # MyArg(nn=[3], a_tuple=('str', 1), encoder='lstm', h_param={}, batch_size=None, adp=False, embedding_dim=100, lr=0.001)

    # `my_arg` can be used in later script with a typed manner, which help of IDEs (type hints and auto completion)
    # ...
    print(f"My network has {len(my_arg.nn)} layers with sizes of {my_arg.nn}.")
    # My network has 1 layers with sizes of [3].


if __name__ == '__main__':
    main()
