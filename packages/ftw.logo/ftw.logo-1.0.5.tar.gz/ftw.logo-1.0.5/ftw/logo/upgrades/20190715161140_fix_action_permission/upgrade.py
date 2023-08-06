from ftw.upgrade import UpgradeStep


class FixActionPermission(UpgradeStep):
    """Fix action permission.
    """

    def __call__(self):
        self.install_upgrade_profile()
